from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm, UserCreateForm
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer
from django.http import Http404
from rest_framework import permissions

def main_page(request):
    return render(request, 'timetracker/main_page.html')


@login_required
def post_list(request):
    posts = Post.objects.filter(author=request.user,
                                published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'timetracker/post_list.html', {'posts': posts})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    return render(request, 'timetracker/post_detail.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'timetracker/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'timetracker/post_edit.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()
    return redirect('post_list')


class RegistrationFormView(FormView):
    form_class = UserCreateForm

    # Посилання на яке переходить користувач вразі успішної реєстрації
    success_url = "/login/"

    # Шаблон, який побачить користувач при відображенні представлення.
    template_name = "timetracker/register.html"

    def form_valid(self, form):
        # Якщо форма коректна, то додаємо користувача
        form.save()

        # Викликаємо метод базового класу
        return super(RegistrationFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm

    template_name = "timetracker/login.html"

    success_url = "/posts/"

    def form_valid(self, form):
        # Отримуємо об'єкт користувача із форми
        self.user = form.get_user()

        # Виконуємо аутентифікацію користувача.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


def logout_(request):
    logout(request)
    return redirect('user_login')


class PostList(APIView):

    permission_classes = (permissions.IsAuthenticated,)
	# permission_classes = (IsAuthenticated,)

    def get(self, request):
        posts = Post.objects.filter(author=request.user,
                                    published_date__lte=timezone.now()).order_by('-published_date')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        snippet = self.get_object(pk)
        serializer = PostSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk):
        snippet = self.get_object(pk)
        serializer = PostSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)