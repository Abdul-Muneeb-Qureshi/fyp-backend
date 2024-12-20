from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from django.conf import settings
from .utils.docx_utils import process_document_file
from .utils.excel_utils import convert_excel_to_json 
from .utils.docx_utils import process_doc_chunks
from .utils.background_task import run_in_background 
from django.core.cache import cache
from uuid import uuid4
from .utils.topic_entitiy_utils import generate_topics_entities
from django.db import connection
from rest_framework import status



class ProcessDocumentView(APIView):
    """
    API to process .docx files and return metadata and chunked text files.
    """ 
    def get(self , request):
        xlsx_file_name = 'ASR_Reports (Tajziakaar).xlsx'
        json_file_name = 'ASR_Reports (Tajziakaar).json'

        xlsx_file_path = os.path.join(settings.MEDIA_ROOT, 'ASR_Tajziakaar Reports', xlsx_file_name)
        json_file_path = os.path.join(settings.MEDIA_ROOT, 'ASR_Tajziakaar Reports', json_file_name)

        ouput_path = os.path.join(settings.MEDIA_ROOT, 'chunks')

        document_folder = os.path.join(settings.MEDIA_ROOT, 'ASR_Tajziakaar Reports')



        # convert_excel_to_json(xlsx_file_path , json_file_path )
        process_doc_chunks(ouput_path , json_file_path , document_folder)


        return Response({"message": "hello!" , "file": ouput_path})
    

class GenerateTopicsEntities(APIView):
    def get(self, request):
        json_file_name = 'ASR_Reports (Tajziakaar).json'
        json_file_path = os.path.join(settings.MEDIA_ROOT, 'ASR_Tajziakaar Reports', json_file_name)
        
        # Generate a unique key for this task
        progress_key = str(uuid4())
        
        # Start the background task
        run_in_background(generate_topics_entities, json_file_path, progress_key)
        
        # Return the progress key to the client
        return Response({"message": "Task started", "progress_key": progress_key})
    

class CheckTaskProgress(APIView):
    def get(self, request, progress_key):
        progress_data = cache.get(progress_key)
        
        if progress_data:
            return Response(progress_data)
        else:
            return Response({"status": "not_found", "message": "Invalid or expired progress key"}, status=404)


class MostFrequentEntityView(APIView):
    def get(self, request, *args, **kwargs):
        query = """
            SELECT t.entity, COUNT(t.entity) AS entity_count
            FROM pipeline_topic t
            JOIN pipeline_video v ON t.video_id = v.id
            WHERE v.published_date BETWEEN '2024-01-01' AND '2024-12-31'
            GROUP BY t.entity
            ORDER BY entity_count DESC
            LIMIT 10;
        """
        try:
            # Execute the query
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()  # Fetch all rows

            # Format the response
            if results:
                data = [
                    {"entity": row[0], "entity_count": row[1]}
                    for row in results
                ]
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No data found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)