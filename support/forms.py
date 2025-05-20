from django import forms
from .models import SupportTicket

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['category', 'subject', 'message', 'image']
        labels = {
            'category': 'Destek Kategorisi',
            'subject': 'Konu Başlığı',
            'message': 'Mesajınız',
            'image': 'Dosya (isteğe bağlı)',
        }
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full bg-white dark:bg-white/10 border border-gray-400 dark:border-gray-600 rounded-lg px-4 py-3 text-sm text-gray-800 dark:text-white focus:outline-none focus:ring-1 focus:ring-gray-600 transition'
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Kısa bir konu başlığı girin',
                'class': 'w-full bg-white dark:bg-white/10 border border-gray-400 dark:border-gray-600 rounded-lg px-4 py-3 text-sm text-gray-800 dark:text-white focus:outline-none focus:ring-1 focus:ring-gray-600 transition'
            }),
            'message': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Detayları açıkça yazın, gerekirse sipariş kodu veya tarih ekleyin.',
                'class': 'w-full bg-white dark:bg-white/10 border border-gray-400 dark:border-gray-600 rounded-lg px-4 py-3 text-sm text-gray-800 dark:text-white focus:outline-none focus:ring-1 focus:ring-gray-600 transition'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full bg-white dark:bg-white/10 border border-gray-400 dark:border-gray-600 rounded-lg px-4 py-3 text-sm text-gray-800 dark:text-white focus:outline-none focus:ring-1 focus:ring-gray-600 transition file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100'
            }),
        }
