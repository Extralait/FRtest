from django.db import models


class Quiz(models.Model):
    """
    Опрос (Модель)
    """
    name = models.CharField(
        verbose_name='Name',
        max_length=256,
    )
    owner = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    models.CharField(
        verbose_name='Name',
        max_length=256,
    )
    is_active = models.BooleanField(
        verbose_name='Is active',
        blank=True,
        default=False
    )
    start_date = models.DateTimeField(
        verbose_name='Start date',
    )
    end_date = models.DateTimeField(
        verbose_name='End date',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        """
        Обработка полей перед сохранением модели
        """
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class Question(models.Model):
    """
    Вопрос (Модель)
    """
    TEXT = 'text'
    CHECKBOX = 'checkbox'
    RADIO = 'radio'

    QUESTION_TYPE_CHOICES = (
        (TEXT, 'Text'),
        (CHECKBOX, 'Checkbox'),
        (RADIO, 'Radio'),
    )
    quiz = models.ForeignKey(
        to='quiz.Quiz',
        on_delete=models.CASCADE
    )
    question_text = models.CharField(
        verbose_name='Question text',
        max_length=2048,
    )
    question_type = models.CharField(
        verbose_name='Verify status',
        max_length=14,
        choices=QUESTION_TYPE_CHOICES,
        default=TEXT
    )
    is_required = models.BooleanField(
        verbose_name='Is required',
        default=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        """
        Обработка полей перед сохранением модели
        """
        self.question_text = self.question_text.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        text = self.question_text

        if len(text) > 100:
            return f'{text[:100] + "..."}'
        else:
            return f'{self.question_text}'


class Choice(models.Model):
    """
    Вариант ответа
    """
    question = models.ForeignKey(
        to='quiz.Question',
        on_delete=models.CASCADE
    )
    title = models.CharField(
        verbose_name='title',
        max_length=1024
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        null=True
    )
    quiz = models.ForeignKey(
        to='quiz.Quiz',
        related_name='answer',
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        to='quiz.Question',
        on_delete=models.CASCADE
    )
    text_answer = models.CharField(
        max_length=2048,
        blank=True,
        null=True
    )
    checkbox_answer = models.ManyToManyField(
        to='quiz.Choice',
        blank=True,
        related_name='checkbox'
    )
    radio_answer = models.ForeignKey(
        to='quiz.Choice',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='radio'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.pk} - {self.user.email}'
