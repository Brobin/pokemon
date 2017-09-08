from django.shortcuts import render


def signup(request):
    if request.user.is_authenticated():
        return redirect('trainers')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('trainer-create')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
