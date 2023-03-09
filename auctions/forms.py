from django import forms
from .models import User, AuctionListing, Bid

class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ('title', 'price', 'starting_bid', 'description', 'picture')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('bid',)
        widgets = {
            'bid': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        self.fields['bid'].label = "Bid Amount"