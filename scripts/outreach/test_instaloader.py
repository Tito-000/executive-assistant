"""Test instaloader sin login — algunos perfiles publicos permiten lectura anonima."""

import instaloader
import json

L = instaloader.Instaloader(
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    download_geotags=False,
    download_comments=False,
    save_metadata=False,
    compress_json=False,
)

USERNAME = "draaurysm"

print(f"Intentando leer @{USERNAME} sin login...")

try:
    profile = instaloader.Profile.from_username(L.context, USERNAME)

    print(f"\nPerfil encontrado:")
    print(f"  Username: {profile.username}")
    print(f"  Full name: {profile.full_name}")
    print(f"  Bio: {profile.biography}")
    print(f"  Followers: {profile.followers}")
    print(f"  Following: {profile.followees}")
    print(f"  Posts count: {profile.mediacount}")
    print(f"  Is business: {profile.is_business_account}")
    print(f"  Business category: {profile.business_category_name}")
    print(f"  External URL: {profile.external_url}")
    print(f"  Is private: {profile.is_private}")

    print(f"\nUltimos posts:")
    count = 0
    for post in profile.get_posts():
        count += 1
        print(f"\n  Post {count}:")
        print(f"    Date: {post.date_utc}")
        print(f"    Likes: {post.likes}")
        print(f"    Caption: {(post.caption or '')[:300]}")
        if count >= 5:
            break

    print(f"\nTotal: {count} posts leidos")

except instaloader.exceptions.LoginRequiredException:
    print("FAIL: Instagram pide login para este perfil. Necesitamos @scout.")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
