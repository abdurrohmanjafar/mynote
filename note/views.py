from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from note.models import Note
from .serializers import GetNoteSerializer

class NoteViews(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id=None):
        if id:
            try:
                found_object = Note.objects.get(id=id)
                if request.user == found_object.user:
                    serialized_object = GetNoteSerializer(found_object)
                    return Response(serialized_object.data, status.HTTP_200_OK)
                else:
                    raise ValueError("user tidak memiliki akses")
            
            except Note.DoesNotExist:
                return Response({'error': 'objek dengan nomor ID {} tidak ditemukan'.format(id)}, status.HTTP_404_NOT_FOUND)

            except ValueError:
                return Response({"error": "user tidak memiliki akses"}, status.HTTP_403_FORBIDDEN)
        
        get_object = Note.objects.filter(user=request.user)
        serialized_object = GetNoteSerializer(get_object, many=True)
        return Response(serialized_object.data, status.HTTP_200_OK)
    
    def post(self, request, id=None):
        try:
            print(request.data)
            data = {
                "title": request.data.get("title", None),
                "text": request.data.get("text", None),
                "user": request.user.id
            }
            if id:
                get_object = Note.objects.get(id=id)
                if get_object.user == request.user:
                    serialized_object = GetNoteSerializer(get_object, data=data, partial=True)
                else:
                    raise ValueError("user tidak memiliki akses")
            else:
                serialized_object = GetNoteSerializer(data=data)

            if serialized_object.is_valid():
                serialized_object.save()
                return Response(serialized_object.data, status.HTTP_200_OK)
            else:
                raise ValueError(serialized_object.errors)

        except ValueError as e:
            return Response({"error": str(e)}, status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "terjadi kesalahan input"}, status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, id=None):
        try:
            if id:
                get_object = Note.objects.get(id=id)
                if request.user == get_object.user:
                    get_object.delete()
                    return Response({"message": "berhasil menghapus objek"}, status.HTTP_200_OK)
                else:
                    raise ValueError("User tidak memiliki akses")
            else:
                raise ValueError("kesalahan URL tujuan")

        except Note.DoesNotExist:
            return Response({"error": "Gagal menghapus objek, objek dengan id {} tidak ditemukan".format(id)}, status.HTTP_400_BAD_REQUEST)

        except ValueError as e:
            return Response({"error": str(e)}, status.HTTP_400_BAD_REQUEST)
