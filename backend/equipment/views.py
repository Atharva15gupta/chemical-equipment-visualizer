from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.middleware.csrf import get_token
from .models import Dataset
from .serializers import DatasetSerializer, UploadResponseSerializer
import pandas as pd
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from datetime import datetime


class DatasetViewSet(viewsets.ModelViewSet):
    """ViewSet for managing datasets"""
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Dataset.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def upload(self, request):
        """Upload and process CSV file"""
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        csv_file = request.FILES['file']
        
        # Validate file extension
        if not csv_file.name.endswith('.csv'):
            return Response(
                {'error': 'File must be a CSV'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Read CSV file
            df = pd.read_csv(csv_file)
            
            # Validate required columns
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            if not all(col in df.columns for col in required_columns):
                return Response(
                    {'error': f'CSV must contain columns: {", ".join(required_columns)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Calculate summary statistics
            total_count = len(df)
            avg_flowrate = float(df['Flowrate'].mean())
            avg_pressure = float(df['Pressure'].mean())
            avg_temperature = float(df['Temperature'].mean())
            type_distribution = df['Type'].value_counts().to_dict()
            
            # Save the file
            csv_file.seek(0)  # Reset file pointer
            file_path = default_storage.save(
                f'uploads/{csv_file.name}',
                ContentFile(csv_file.read())
            )
            
            # Create dataset record
            dataset = Dataset.objects.create(
                user=request.user,
                filename=csv_file.name,
                total_count=total_count,
                avg_flowrate=avg_flowrate,
                avg_pressure=avg_pressure,
                avg_temperature=avg_temperature,
                type_distribution=type_distribution,
                csv_file=file_path
            )
            
            # Cleanup old datasets (keep only last 5)
            Dataset.cleanup_old_datasets(request.user, keep_count=5)
            
            # Prepare response data
            data_records = df.to_dict('records')
            
            response_data = {
                'message': 'File uploaded successfully',
                'dataset_id': dataset.id,
                'summary': {
                    'total_count': total_count,
                    'avg_flowrate': round(avg_flowrate, 2),
                    'avg_pressure': round(avg_pressure, 2),
                    'avg_temperature': round(avg_temperature, 2),
                    'type_distribution': type_distribution
                },
                'data': data_records
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Error processing file: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        """Generate and download PDF report for a dataset"""
        try:
            dataset = self.get_object()
            
            # Create PDF in memory
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            # Title
            title = Paragraph(
                f"<b>Chemical Equipment Report</b><br/>{dataset.filename}",
                styles['Title']
            )
            elements.append(title)
            elements.append(Spacer(1, 0.3*inch))
            
            # Summary section
            summary_text = f"""
            <b>Summary Statistics</b><br/>
            Upload Date: {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M')}<br/>
            Total Equipment Count: {dataset.total_count}<br/>
            Average Flowrate: {dataset.avg_flowrate:.2f}<br/>
            Average Pressure: {dataset.avg_pressure:.2f}<br/>
            Average Temperature: {dataset.avg_temperature:.2f}<br/>
            """
            elements.append(Paragraph(summary_text, styles['Normal']))
            elements.append(Spacer(1, 0.3*inch))
            
            # Type distribution table
            elements.append(Paragraph("<b>Equipment Type Distribution</b>", styles['Heading2']))
            elements.append(Spacer(1, 0.1*inch))
            
            type_data = [['Equipment Type', 'Count']]
            for eq_type, count in dataset.type_distribution.items():
                type_data.append([eq_type, str(count)])
            
            type_table = Table(type_data)
            type_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(type_table)
            
            # Build PDF
            doc.build(elements)
            buffer.seek(0)
            
            # Create response
            response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="report_{dataset.id}.pdf"'
            return response
            
        except Exception as e:
            import traceback
            print("PDF Generation Error:", str(e))
            traceback.print_exc()
            return Response(
                {'error': f'Error generating PDF: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get last 5 uploaded datasets"""
        datasets = self.get_queryset()[:5]  # Limit to 5 most recent
        serializer = self.get_serializer(datasets, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user"""
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create_user(username=username, password=password, email=email)
    return Response(
        {'message': 'User created successfully', 'username': username},
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Login user"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        login(request, user)
        return Response({
            'message': 'Login successful',
            'username': username
        })
    else:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@ensure_csrf_cookie
def get_csrf_token(request):
    """Get CSRF token - sets the CSRF cookie"""
    return JsonResponse({'csrfToken': get_token(request)})

