from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Person, Product
from .forms import PersonForm

@login_required
def persons_list(request):
  search = request.GET.get('pesquisa', None)

  # last_name_search = request.GET.get('last_name', None)
  # first_name_search = request.GET.get('first_name', None)

  # Busca de 2 campos com case sensitive
  # if last_name_search or firs_name_search
  #   persons = Person.objects.filter(first_name__icontains=first_name_search, last_name__icontains=last_name_search)

  if search:
    persons = Person.objects.all()
    persons = persons.filter(first_name=search)
  else:
    persons = Person.objects.all()

  return  render(request, 'clientes/persons_list.html', {'persons': persons})

@login_required
def persons_new(request):
  form = PersonForm(request.POST or None, request.FILES or None)

  if form.is_valid():
    form.save()
    return redirect('person_list')

  return render(request, 'clientes/person_form.html', {'form': form})

@login_required
def persons_update(request, id):
  person = get_object_or_404(Person, pk=id)
  form = PersonForm(request.POST or None, request.FILES or None, instance=person)

  if form.is_valid():
    form.save()
    return redirect('person_list')

  return render(request, 'clientes/person_form.html', {'form': form})

@login_required
def persons_delete(request, id):
  person = get_object_or_404(Person, pk=id)
  form = PersonForm(request.POST or None, request.FILES or None, instance=person)

  if request.method == 'POST':
    person.delete()
    return redirect('person_list')
  
  return render(request, 'clientes/person_delete_confirm.html', {'person': person })


class PersonList(ListView):
  model = Person


class PersonDetail(DetailView):
  model = Person


  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['now'] = timezone.now()
    return context


class PersonCreate(CreateView):
  model = Person
  fields = ['first_name', 'last_name', 'age', 'salary', 'bio', 'photo',]
  success_url = '/clientes/person_list'


class PersonUpdate(UpdateView):
  model = Person
  fields = ['first_name', 'last_name', 'age', 'salary', 'bio', 'photo',]
  success_url = reverse_lazy('person_list_cbv')


class PersonDelete(DeleteView):
  model = Person
  fields = ['first_name', 'last_name', 'age', 'salary', 'bio', 'photo',]
  success_url = reverse_lazy('person_list_cbv')


class ProdutoBulk(View):
  def get(self, request):
    products = ['Banana', 'Maça', 'Limão', 'Laranja', 'Pera', 'Melancia']
    products_list = []

    for product in products:
      p = Product(description=product, price=10)
      products_list.append(p)

    Produto.objects.bulk_create(product_list)

    return HttpResponse('Funcionou')  