from django.db import models

# Create your models here.
class Author(models.Model):
    author_id = models.AutoField(primary_key=True, verbose_name='작가 ID')
    author_name = models.CharField(max_length=200, verbose_name='작가 이름')
    birth_date = models.DateField(verbose_name='생년월일', null=True, blank=True)
    death_date = models.DateField(verbose_name='사망일자', null=True, blank=True)
    nation_cd = models.ForeignKey('resume.Comm_code', related_name='fk_author1', on_delete=models.SET_NULL, null=True, db_column='nation_cd',  verbose_name='국적')
    summary = models.CharField(max_length=4000, null=True, blank=True, verbose_name='약력')

    USE_YN_DIV = (
        ('Y', 'Y'),
        ('N', 'N'),
    )

    book_find_yn = models.CharField(max_length=1, choices=USE_YN_DIV, default='Y', verbose_name='책 자동 찾기 여부')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)
    update_dt = models.DateTimeField(auto_now=True, verbose_name='수정일시', null=True, blank=True)
    create_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='생성자id')
    update_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='수정자id')

    class Meta:
        managed = True

    def __str__(self):
        """String for representing the Model object."""
        return self.author_name

class Book(models.Model):
    book_id = models.AutoField(primary_key=True, verbose_name='책 ID')
    isbn = models.CharField(max_length=20, verbose_name='ISBN', null=True, blank=True)
    book_name = models.CharField(max_length=200, verbose_name='책 이름')
    author_id = models.ForeignKey('Author', related_name='fk_book1', on_delete=models.SET_NULL, null=True,
                                  db_column='author_id', verbose_name='저자')
    genre_cd = models.ForeignKey('resume.Comm_code', related_name='fk_book2', on_delete=models.SET_NULL, null=True, db_column='genre_cd',  verbose_name='장르')
    publisher_name = models.CharField(max_length=200, verbose_name='출판사', null=True, blank=True)

    publish_date = models.DateField(verbose_name='출판일자', null=True, blank=True)
    summary = models.CharField(max_length=4000, null=True, blank=True, verbose_name='책소개')
    book_url = models.CharField(max_length=400, verbose_name='관련URL', null=True, blank=True)

    USE_YN_DIV = (
        ('Y', 'Y'),
        ('N', 'N'),
    )

    auto_update_yn = models.CharField(max_length=1, choices=USE_YN_DIV, default='N',  verbose_name='자동 update 완료 여부')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)
    update_dt = models.DateTimeField(auto_now=True, verbose_name='수정일시', null=True, blank=True)
    create_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='생성자id')
    update_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='수정자id')

    class Meta:
        managed = True

    def __str__(self):
        """String for representing the Model object."""
        return self.book_name
