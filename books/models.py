from django.db import models

# Create your models here.
class Author(models.Model):
    author_id = models.AutoField(primary_key=True, verbose_name='작가 ID')
    author_name = models.CharField(max_length=200, verbose_name='작가 이름')
    birth_date = models.DateField(verbose_name='생년월일', null=True)
    nation_cd = models.ForeignKey('resume.Comm_code', related_name='fk_author1', on_delete=models.SET_NULL, null=True, db_column='nation_cd',  verbose_name='국적')
    summary = models.CharField(max_length=4000, null=True, blank=True, verbose_name='약력')
    book_find_yn = models.CharField(max_length=1, verbose_name='책찾기 여부')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='생성일시', null=True, blank=True)
    update_dt = models.DateTimeField(auto_now=True, verbose_name='수정일시', null=True, blank=True)
    create_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='생성자id')
    update_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='수정자id')

    class Meta:
        managed = True

    def __str__(self):
        """String for representing the Model object."""
        return self.author_name
