from rest_framework.generics import ListAPIView
from .models import *
from .serializers import VideoSerializer, PollSerializer, ClassroomDataSerializer, MiniGameBakgroudnSerializer
from rest_framework.permissions import AllowAny as A
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncDay
from apps.account.authentication import BlacklistAwareJWTAuthentication
from apps.account.models import User
from apps.forms.models import *
from apps.guardians.models import *
from apps.products.models import *
from apps.quiz.models import *
from apps.videos.models import *
from datetime import datetime, timedelta
class VideoListAPIView(ListAPIView):
    permission_classes = [A]
    authentication_classes = []
    queryset = Video.objects.all().order_by("-id")
    serializer_class = VideoSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        for permission in permissions:
            print(f"Permission: {permission}")
        return permissions

class PollListAPIView(ListAPIView):
    authentication_classes = []
    permission_classes = [A]
    queryset = Poll.objects.all().order_by("-created_at")
    serializer_class = PollSerializer
    
class PollOfWeek(APIView):
    permission_classes=[A]
    
    def get(self, request):
        poll = Poll.objects.get(poll_of_week=True)
        serialiser = PollSerializer(poll)
        return Response(serialiser.data)

class PollResultsAPIView(APIView):
    permission_classes = [A]
    authentication_classes = []
    def get(self, request, pk):
        try:
            poll = Poll.objects.get(id=pk)
        except Poll.DoesNotExist:
            return Response({"detail": "Poll not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PollSerializer(poll)
        return Response(serializer.data)
class VideoDetailAPIView(APIView):
    permission_classes = [A]
    authentication_classes = []
    def get(self, request, pk):
        try:
            video = Video.objects.get(id=pk)
        except Video.DoesNotExist:
            return Response({"detail": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VideoSerializer(video)
        return Response(serializer.data)

class PollVoteAPIView(APIView):
    permission_classes = [A]
    authentication_classes = []

    def post(self, request):
        poll_id = request.data.get("poll_id")
        option_id = request.data.get("option_id")
        device_id = (request.data.get("device_id") or "").strip()
        user = getattr(request, "user", None)
        if user and getattr(user, "is_authenticated", False):
            user = user
        else:
            user = None
            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ", 1)[1].strip()
                if token:
                    jwt_auth = BlacklistAwareJWTAuthentication()
                    try:
                        validated_token = jwt_auth.get_validated_token(token)
                        user = jwt_auth.get_user(validated_token)
                    except Exception:
                        user = None

        if not poll_id or not option_id:
            return Response(
                {"detail": "poll_id and option_id are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            poll = Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            return Response({"detail": "Poll not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            option = PollOption.objects.get(id=option_id, poll_id=poll.id)
        except PollOption.DoesNotExist:
            return Response({"detail": "Invalid option for this poll"}, status=status.HTTP_400_BAD_REQUEST)

        if user:
            if PollVote.objects.filter(poll_id=poll.id, user=user).exists():
                return Response(
                    {"detail": "You have already voted in this poll."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            PollVote.objects.create(
                poll=poll,
                option=option,
                user=user,
            )
        else:
            if not device_id:
                return Response(
                    {"detail": "device_id is required for guest users"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if PollVote.objects.filter(poll_id=poll.id, device_id=device_id).exists():
                return Response(
                    {"detail": "This device has already voted in this poll."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            PollVote.objects.create(
                poll=poll,
                option=option,
                device_id=device_id,
            )

        return Response(PollSerializer(poll).data)
    
    
from django.db.models import F

def dashboard_callback(request, context):
    """
    Callback to prepare custom variables for index template which is used as dashboard
    template. It can be overridden in application by creating custom admin/index.html.
    """
    # Stats
    total_users = User.objects.count()
    total_orders = Order.objects.count()
    
    # Fix revenue calculation: sum(price * quantity + delivery) for paid orders
    revenue_data = Order.objects.filter(paid=True).aggregate(
        revenue=Sum(F('price') * F('quantity') + F('delivery_charge'))
    )
    total_revenue = revenue_data['revenue'] or 0

    total_products = Product.objects.count() + Books.objects.count()
    total_videos = Video.objects.count()
    total_guardians = Guardian.objects.count()
    total_quiz_sets = QuizSet.objects.count()
    total_polls = Poll.objects.count()
    total_partnership = PartnershipInquary.objects.count()
    total_newsletter = NewsletterSubscription.objects.count()
    total_kit_requests = ALHeraKitRequest.objects.count()

    # Charts data
    # Users over time (last 12 months)
    users_over_time = User.objects.annotate(month=TruncMonth('date_joined')).values('month').annotate(count=Count('id')).order_by('month')
    users_labels = [item['month'].strftime('%b %Y') for item in users_over_time if item['month']]
    users_data = [item['count'] for item in users_over_time if item['month']]

    # Orders by status
    orders_by_status = Order.objects.values('order_status').annotate(count=Count('id')).order_by('order_status')
    orders_status_labels = [item['order_status'].capitalize() for item in orders_by_status]
    orders_status_data = [item['count'] for item in orders_by_status]

    # Products by category
    products_by_category = Product.objects.values('category').annotate(count=Count('id')).order_by('category')
    product_categories = {item['category']: item['count'] for item in products_by_category}
    # Ensure keys exist even if None/Empty
    clean_categories = {}
    for k, v in product_categories.items():
        key_name = k if k else "Uncategorized"
        # map choice label if possible, or just capitalize
        if key_name == "gear": key_name = "Guardian Gear"
        elif key_name == "other": key_name = "Others"
        clean_categories[key_name] = v
        
    books_count = Books.objects.count()
    product_labels = list(clean_categories.keys()) + ['Books']
    product_data = list(clean_categories.values()) + [books_count]

    # Videos by type
    videos_by_type = Video.objects.values('video_type').annotate(count=Count('id')).order_by('video_type')
    video_labels = [item['video_type'].capitalize() for item in videos_by_type]
    video_data = [item['count'] for item in videos_by_type]

    # Guardians by nationality
    guardians_by_nationality = Guardian.objects.values('nationality').annotate(count=Count('id')).order_by('-count')[:10]  # Top 10
    guardian_labels = [item['nationality'] for item in guardians_by_nationality]
    guardian_data = [item['count'] for item in guardians_by_nationality]

    # Quiz scores distribution
    quiz_scores = QuizAttempt.objects.values_list('score', flat=True)
    score_bins = [0, 20, 40, 60, 80, 100]
    score_labels = ['0-20', '21-40', '41-60', '61-80', '81-100']
    score_data = [sum(1 for s in quiz_scores if bin_start <= s < bin_end) for bin_start, bin_end in zip(score_bins[:-1], score_bins[1:])]
    # Handle exactly 100 separately or include in last bin
    # Current logic excludes 100 in range. Let's fix last bin to include 100.
    score_data[-1] += sum(1 for s in quiz_scores if s == 100)

    # Recent activity
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_attempts = QuizAttempt.objects.select_related('user', 'quiz_set').order_by('-completed_at')[:5]
    
    # Recent Forms
    recent_partnership = PartnershipInquary.objects.order_by('-created_at')[:5]
    recent_kit_requests = ALHeraKitRequest.objects.order_by('-id')[:5] # No created_at in kit request, use id

    context.update({
        # Stats
        'total_users': total_users,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'total_videos': total_videos,
        'total_guardians': total_guardians,
        'total_quiz_sets': total_quiz_sets,
        'total_polls': total_polls,
        'total_partnership': total_partnership,
        'total_newsletter': total_newsletter,
        'total_kit_requests': total_kit_requests,

        # Charts
        'users_labels': users_labels,
        'users_data': users_data,
        'orders_status_labels': orders_status_labels,
        'orders_status_data': orders_status_data,
        'product_labels': product_labels,
        'product_data': product_data,
        'video_labels': video_labels,
        'video_data': video_data,
        'guardian_labels': guardian_labels,
        'guardian_data': guardian_data,
        'score_labels': score_labels,
        'score_data': score_data,

        # Recent
        'recent_orders': recent_orders,
        'recent_users': recent_users,
        'recent_attempts': recent_attempts,
        'recent_partnership': recent_partnership,
        'recent_kit_requests': recent_kit_requests,
    })
    return context


class ClassroomDataAPIView(APIView):
    permission_classes = [A]
    authentication_classes = []

    def get(self, request, classroom_type):
        classroom_item = classroomData.objects.filter(types=classroom_type).order_by("-id").first()
        if not classroom_item:
            return Response(
                {"detail": f"No classroom data found for type '{classroom_type}'"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ClassroomDataSerializer(classroom_item, context={"request": request})
        return Response(serializer.data)

class ClassroomDataAllAPIView(APIView):
    permission_classes = [A]
    authentication_classes = []

    def get(self, request):
        classroom_items = classroomData.objects.filter().order_by("-id")
        serializer = ClassroomDataSerializer(classroom_items, many=True, context={"request": request})
        return Response(serializer.data)

class MiniGameBakgroudnAPIView(APIView):
    permission_classes = [A]
    authentication_classes = []

    def get(self, request):
        minigame_backgrounds = MiniGameBakgroudn.objects.all().order_by("-id")
        serializer = MiniGameBakgroudnSerializer(minigame_backgrounds, many=True, context={"request": request})
        return Response(serializer.data)
