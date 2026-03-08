from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Exists, OuterRef
from django.http import HttpRequest
from .models import Profile, Post

MOCK_FEED = {
    "current_user": {
        "name": "Marcio",
        "username": "marcio",
        "initials": "MM",
        "avatar_url": None,
        "avatar_color": "135deg,#c84b2f,#e87d5a",
        "is_verified": False,
        "followers": 1200,
        "following": 248,
        "posts_count": 934,
        "bio": "Building things on the web. Interested in design, systems, and the odd intersection of both.",
    },

    "posts": [
        {
            "id": 1,
            "body": "Just shipped a massive redesign of our onboarding flow. Conversion is up +38% in the first week. The key? We removed 6 steps nobody actually needed. Less is genuinely more. #DesignThinking #ProductDesign",
            "time": "2h",
            "likes_count": 1400,
            "comments_count": 89,
            "reposts_count": 312,
            "liked": False,
            "reposted": False,
            "attachment": "https://placehold.co/600x200/e8f0ff/2f6bc8?text=Onboarding+Redesign",
            "quote": None,
            "author": {
                "name": "Aline Leconte",
                "username": "aline_lec",
                "initials": "AL",
                "avatar_url": None,
                "avatar_color": "135deg,#2f6bc8,#5b9be8",
                "is_verified": True,
            },
        },
        {
            "id": 2,
            "body": "This is exactly the problem with most B2B SaaS pricing pages. You're burying your best tier.",
            "time": "5h",
            "likes_count": 872,
            "comments_count": 54,
            "reposts_count": 201,
            "liked": True,
            "reposted": False,
            "attachment": None,
            "quote": {
                "body": "Why do companies hide their enterprise plan behind a 'Contact Sales' button?? Just show me the price.",
                "author": {
                    "name": "Sarah Mitchell",
                    "username": "sarahmitch",
                },
            },
            "author": {
                "name": "Rohan Kapoor",
                "username": "rohandev",
                "initials": "RK",
                "avatar_url": None,
                "avatar_color": "135deg,#2a7a4b,#4db87a",
                "is_verified": False,
            },
        },
        {
            "id": 3,
            "body": "Hot take: your landing page copy is too clever. Stop trying to sound smart. Clarity converts. Cleverness confuses. I rewrote a client's hero in 20 minutes — CTR went from 2.1% to 6.8%. #Copywriting",
            "time": "8h",
            "likes_count": 3200,
            "comments_count": 214,
            "reposts_count": 889,
            "liked": False,
            "reposted": True,
            "attachment": None,
            "quote": None,
            "author": {
                "name": "Nadia Wolff",
                "username": "nadiaw",
                "initials": "NW",
                "avatar_url": None,
                "avatar_color": "135deg,#c84b2f,#f07050",
                "is_verified": True,
            },
        },
        {
            "id": 4,
            "body": "Spent the weekend reading old Unix manuals from the 70s. These people were solving the exact same architecture problems we 'discovered' in 2015. Nothing is new. Everything is a remix. #SoftwareEngineering",
            "time": "12h",
            "likes_count": 607,
            "comments_count": 41,
            "reposts_count": 129,
            "liked": False,
            "reposted": False,
            "attachment": None,
            "quote": None,
            "author": {
                "name": "Jonas Laurent",
                "username": "jonasl",
                "initials": "JL",
                "avatar_url": None,
                "avatar_color": "135deg,#7a2a7a,#b470b4",
                "is_verified": False,
            },
        },
        {
            "id": 5,
            "body": "The best UI pattern nobody talks about: progressive disclosure. Show only what's needed, reveal complexity on demand. It's why great apps feel effortless even when they do a lot.",
            "time": "1d",
            "likes_count": 2100,
            "comments_count": 173,
            "reposts_count": 544,
            "liked": False,
            "reposted": False,
            "attachment": "https://placehold.co/600x200/fff8e8/c87a2f?text=Progressive+Disclosure",
            "quote": None,
            "author": {
                "name": "Yuki Matsuda",
                "username": "yukimat",
                "initials": "YM",
                "avatar_url": None,
                "avatar_color": "135deg,#c87a2f,#e8b060",
                "is_verified": True,
            },
        },
    ],

    "suggested_users": [
        {
            "name": "Theo Huang",
            "username": "theohuang",
            "initials": "TH",
            "avatar_url": None,
            "avatar_color": "135deg,#2f6bc8,#5b9be8",
            "is_verified": False,
            "following": False,
        },
        {
            "name": "Elena Cruz",
            "username": "elenacruz",
            "initials": "EC",
            "avatar_url": None,
            "avatar_color": "135deg,#2a7a4b,#4db87a",
            "is_verified": True,
            "following": True,
        },
        {
            "name": "Oscar Brandt",
            "username": "oscarb",
            "initials": "OB",
            "avatar_url": None,
            "avatar_color": "135deg,#7a2a7a,#b470b4",
            "is_verified": False,
            "following": False,
        },
        {
            "name": "Lena Fischer",
            "username": "lenaf",
            "initials": "LF",
            "avatar_url": None,
            "avatar_color": "135deg,#c87a2f,#e8b060",
            "is_verified": False,
            "following": False,
        },
    ],

    "trending": [
        {"category": "Design", "tag": "#DesignSystems", "posts": "14.2k"},
        {"category": "Technology", "tag": "#OpenSource", "posts": "9.8k"},
        {"category": "Product", "tag": "#ShipIt", "posts": "6.1k"},
        {"category": "Engineering", "tag": "#WebPerf", "posts": "4.4k"},
    ],
}

@login_required
def dashboard_view(request):
    context = {"posts": MOCK_FEED["posts"]}
    return render(request, "profiles/dashboard.html", context)

@login_required
def create_post(request:HttpRequest):
    user = request.user
    form = Post(request.POST, request.FILES)

    if not form.is_valid():
        return JsonResponse({'errors':form.errors}, status=400)
    
    with transaction.atomic():
        post = form.save(commit=False)
        post.author = request.user
        post.save()

    return JsonResponse({'id': post.id}, status=201)


    #get current logged in user
    #get the request.body information
    #parse data (body and image)
    #(Optional) review post-body for malicious send and post-attachment
    #Save information in db with ACID standards
    #Return 
    
