from django.db import models


class User(models.Model):
    telegram_id = models.CharField(max_length=20, unique=True, verbose_name='Telegram ID')
    phone_number = models.CharField(max_length=15, verbose_name='Telefon raqami')
    full_name = models.CharField(max_length=120, verbose_name='Ism va Familiya')
    date_of_birth = models.CharField(max_length=120, verbose_name="Tug'ulgan sana")
    city = models.CharField(max_length=120, verbose_name="Tumani")
    information = models.CharField(max_length=120, verbose_name="Ma'lumoti")
    languages = models.CharField(max_length=120, verbose_name="Til bilishi")
    description = models.TextField(blank=True, null=True, verbose_name="Adminlar kiritishi uchun malumot")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ro'yxatdan o'tgan vaqti")
    ball = models.CharField(max_length=120, verbose_name="Testdan to'plagan bali")

    class Meta:
        verbose_name = "Kondinantlar"
        verbose_name_plural = "Kondinantlar"
        ordering = ["-created_at"]

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class Vakansiya(models.Model):
    class Answer(models.IntegerChoices):
        HA = 0, "HA"
        YOQ = 1, "YO'Q"

    name = models.CharField(max_length=120, verbose_name="Vakansiya nomi")
    description = models.TextField(null=True, blank=True, verbose_name="Vakansiya haqida ma'lumot")
    photo = models.ImageField(upload_to='media/vakansiya/', verbose_name="Rasm")
    status = models.BooleanField(default=False, verbose_name="Vakansiya Holati")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Vaqti")
    question1 = models.CharField(max_length=150, verbose_name="1-chi Test savoli")
    answer1 = models.IntegerField(choices=Answer.choices, default=Answer.HA, verbose_name="To'g'ri javobni tanlang")
    question2 = models.CharField(max_length=150, verbose_name="2-chi Test savoli")
    answer2 = models.IntegerField(choices=Answer.choices, default=Answer.HA, verbose_name="To'g'ri javobni tanlang")
    question3 = models.CharField(max_length=150, verbose_name="3-chi Test savoli")
    answer3 = models.IntegerField(choices=Answer.choices, default=Answer.HA, verbose_name="To'g'ri javobni tanlang")
    question4 = models.CharField(max_length=150, verbose_name="4-chi Test savoli")
    answer4 = models.IntegerField(choices=Answer.choices, default=Answer.HA, verbose_name="To'g'ri javobni tanlang")

    class Meta:
        verbose_name = "Vakansiya"
        verbose_name_plural = "Vakansiyalar"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class VakansiyaRU(models.Model):
    class Answer(models.IntegerChoices):
        HA = 0, "да"
        YOQ = 1, "Нет"

    name = models.CharField(max_length=120, verbose_name="Название вакансии")
    description = models.TextField(null=True, blank=True, verbose_name="Информация о вакансии")
    photo = models.ImageField(upload_to='media/vakansiya/', verbose_name="Фото")
    status = models.BooleanField(default=False, verbose_name="Статус Вакансии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время")
    question1 = models.CharField(max_length=150, verbose_name="1-й тестовый вопрос")
    answer1 = models.IntegerField(choices=Answer.choices, default=Answer.HA, verbose_name="Выберите правильный ответ")
    question2 = models.CharField(max_length=150, verbose_name="2-й тестовый вопрос")
    answer2 = models.IntegerField(choices=Answer.choices, default=Answer.HA, verbose_name="Выберите правильный ответ")
    question3 = models.CharField(max_length=150, verbose_name="3-й тестовый вопрос")
    answer3 = models.IntegerField(choices=Answer.choices, default=Answer.HA, verbose_name="Выберите правильный ответ")
    question4 = models.CharField(max_length=150, verbose_name="4-й тестовый вопрос")
    answer4 = models.IntegerField(choices=Answer.choices, default=Answer.HA, verbose_name="Выберите правильный ответ")

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

