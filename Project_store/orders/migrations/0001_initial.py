# Generated by Django 4.2.6 on 2023-12-05 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_no', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ref number')),
                ('full_name', models.CharField(max_length=50, null=True, verbose_name='Customer name')),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('address1', models.CharField(max_length=250, null=True)),
                ('address2', models.CharField(blank=True, max_length=250, null=True)),
                ('country', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('contact_no', models.CharField(max_length=100, null=True, verbose_name='Contact nº')),
                ('post_code', models.CharField(max_length=20, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('shipping', models.DecimalField(decimal_places=2, default='11.50', max_digits=5, null=True, verbose_name='Shipping')),
                ('total_paid', models.DecimalField(decimal_places=2, help_text='Shipping price included 11.50', max_digits=6, verbose_name='Total')),
                ('order_key', models.CharField(blank=True, max_length=200, null=True)),
                ('billing_status', models.BooleanField(default=False, verbose_name='Paid')),
                ('billing_date', models.DateTimeField(blank=True, null=True, verbose_name='Billing at')),
                ('saved_later', models.BooleanField(default=False, help_text='saved order for later', verbose_name='Saved')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Price €')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity(unit)')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
            ],
        ),
    ]
