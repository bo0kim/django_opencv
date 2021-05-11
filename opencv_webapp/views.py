from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import SimpleUploadForm, ImageUploadForm
from django.conf import settings
from .cv_function import cv_detect_face

# Create your views here.
def first_view(request):
    return render(request, 'opencv_webapp/first_view.html', {})

def simple_upload(request):
    if request.method == 'POST': # 사용자가 form 태그 내부의 submit 버튼을 클릭하여 데이터를 제출했을 시
        # print(request.POST)
        # print(request.FILES)
        form = SimpleUploadForm(request.POST, request.FILES) # 빈 양식을 만든 후 사용자가 업로드한 데이터를 채워, 채워진 양식을 만듬

        if form.is_valid():
            myfile = request.FILES['image'] # image : HTML input tag-name attribute value
            # print(myfile) # ses.jpg

            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile) # 업로드된 이미지의 경로명 & 이미지 파일 객체 자체
            # print(myfile.name) # 경로명 포함 파일명 : ses.jpg
            # print(filename) # 경로명 포함 파일명 : ses.jpg

            uploaded_file_url = fs.url(filename)
            # print(uploaded_file_url)

            context = {'form':form, 'uploaded_file_url':uploaded_file_url}
            return render(request, 'opencv_webapp/simple_upload.html', context)

    else: # request.method == 'GET'
        form = SimpleUploadForm() # 비어있는 양식
        context = {'form':form}
        return render(request, 'opencv_webapp/simple_upload.html', context)

def detect_face(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save() # 실제로 form에 채워져있는 데이터 저장.
            # row = form.save(commit=False) # 양식 임시저장
            # row.description = row.description.upper()
            # row.save() # 하나의 행 리턴값을 save. form.save()와 큰 차이는 X
            # row = form.save() # 문제 없을 시 그냥 저장가능

            imageURL = settings.MEDIA_URL + form.instance.document.name
            # imageURL = post.document.url
            cv_detect_face(settings.MEDIA_ROOT_URL + imageURL)

            print('********************')
            print('form.instance : ', form.instance)
            print('form.instance.document : ', form.instance.document)
            print('form.instance.document.name : ', form.instance.document.name)
            print('vs post.document : ', post.document)
            print('vs post.document.url : ', post.document.url)
            print()
            print('settings.MEDIA_URL :', settings.MEDIA_URL)
            print('imageURL :', imageURL)

            context = {'form':form, 'post':post}
            return render(request, 'opencv_webapp/detect_face.html', context)
    else: # request.method == 'GET'
        form = ImageUploadForm()
        return render(request, 'opencv_webapp/detect_face.html', {'form':form})
