from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import check_test_results


class TestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, test_id):
        results = check_test_results(request.user, request.data, test_id)

        # Здесь можно сохранить результаты в базу
        return Response({
            'status': 'success',
            'results': results,
            'text_answers_require_review': any(
                detail.get('status') == 'pending'
                for detail in results['details'].values()
            )
        })
