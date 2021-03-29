from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns

# Create your models here.
class Log(models.Model):
    log_id = models.AutoField(primary_key=True, verbose_name='log ID')
    client_ip = models.CharField(max_length=200, null=True, blank=True, verbose_name='client ip')
    log_gb = models.CharField(max_length=200, null=True, blank=True, verbose_name='로그 구분')
    request_info = models.CharField(max_length=2000, null=True, blank=True, verbose_name='request정보')
    user = models.CharField(max_length=200, null=True, blank=True, verbose_name='user정보')
    lat = models.CharField(max_length=2000, null=True, blank=True, verbose_name='위도')
    long = models.CharField(max_length=2000, null=True, blank=True, verbose_name='경도')
    state = models.CharField(max_length=2000, null=True, blank=True, verbose_name='state')
    city = models.CharField(max_length=2000, null=True, blank=True, verbose_name='city')
    addr = models.CharField(max_length=2000, null=True, blank=True, verbose_name='주소')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)

    class Meta:
        managed = True

    def __str__(self):
        """String for representing the Model object."""
        return self.client_ip


class Author(models.Model):
    author_id = models.AutoField(primary_key=True, verbose_name='작가 ID')
    author_name = models.CharField(max_length=200, verbose_name='작가')

    USE_YN_DIV = (
        ('Y', 'Y'),
        ('N', 'N'),
    )

    recommend_yn = models.CharField(max_length=1, choices=USE_YN_DIV, default='Y', verbose_name='추천 여부')
    input_name = models.CharField(max_length=200, verbose_name='추천인', null=True, blank=True)
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)
    update_dt = models.DateTimeField(auto_now=True, verbose_name='수정일시', null=True, blank=True)
    create_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='생성자id')
    update_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='수정자id')

    class Meta:
        managed = True

    def __str__(self):
        """String for representing the Model object."""
        return self.author_name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('author_update', args=[str(self.author_id)])

class Book(models.Model):
    book_id = models.AutoField(primary_key=True, verbose_name='책 ID')
    book_name = models.CharField(max_length=200, verbose_name='도서명')
    author_name = models.CharField(max_length=200, verbose_name='작가')
    genre_cd = models.ForeignKey('resume.Comm_code', related_name='fk_book2', on_delete=models.SET_NULL, null=True, db_column='genre_cd',  verbose_name='장르')
    summary = models.CharField(max_length=4000, null=True, blank=True, verbose_name='책소개')

    USE_YN_DIV = (
        ('Y', 'Y'),
        ('N', 'N'),
    )

    recommend_yn = models.CharField(max_length=1, choices=USE_YN_DIV, default='Y',  verbose_name='추천 여부')
    input_name = models.CharField(max_length=200, verbose_name='추천인', null=True, blank=True)
    read_date = models.DateField(verbose_name='완독일자', null=True)

    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)
    update_dt = models.DateTimeField(auto_now=True, verbose_name='수정일시', null=True, blank=True)
    create_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='생성자id')
    update_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='수정자id')

    class Meta:
        managed = True

    def __str__(self):
        """String for representing the Model object."""
        return self.book_name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book_update', args=[str(self.book_id)])


class Author_book(models.Model):
    Author_book_id = models.AutoField(primary_key=True, verbose_name='작가 도서 ID')
    author_id = models.IntegerField(null=True, blank=True, verbose_name='작가 ID')
    author_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='작가')
    book_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='도서명')
    pub_date = models.CharField(max_length=20, null=True, blank=True, verbose_name='출판일')
    image_url = models.CharField(max_length=500, null=True, blank=True, verbose_name='이미지URL')
    book_link_info = models.CharField(max_length=500, null=True, blank=True, verbose_name='도서링크정보')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)
    update_dt = models.DateTimeField(auto_now=True, verbose_name='수정일시', null=True, blank=True)
    create_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='생성자id')
    update_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='수정자id')

    class Meta:
        managed = True

    def __str__(self):
        """String for representing the Model object."""
        return self.book_name


class Best_book(models.Model):
    best_book_id = models.AutoField(primary_key=True, verbose_name='베스트북 ID')
    site = models.CharField(max_length=200, null=True, blank=True, verbose_name='작가')
    genre = models.CharField(max_length=200, null=True, blank=True, verbose_name='장르')
    rank = models.IntegerField(null=True, blank=True, verbose_name='순위')
    book_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='도서명')
    author_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='작가')
    publisher = models.CharField(max_length=200, null=True, blank=True, verbose_name='출판사')
    book_url = models.CharField(max_length=400, null=True, blank=True, verbose_name='도서URL')
    book_info = models.CharField(max_length=4000, null=True, blank=True, verbose_name='도서정보')
    image_url = models.CharField(max_length=500, null=True, blank=True, verbose_name='이미지URL')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)

    class Meta:
        managed = True

    def __str__(self):
        """String for representing the Model object."""
        return self.book_name
