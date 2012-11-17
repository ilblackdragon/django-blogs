from django.conf import settings

POST_NAME_MIN_LENGTH = getattr(settings, 'BLOG_POST_NAME_MIN_LENGTH', 3)
SHORT_POST_MAX_LENGTH = getattr(settings, 'BLOG_SHORT_POST_MAX_LENGTH', 2048)
CUT_MAX_LENGTH = getattr(settings, 'BLOG_CUT_MAX_LENGTH', 2048)
CUT_TAG = getattr(settings, 'BLOG_CUT_TAG', '<hr class="redactor_cut"')
CUT_TAG_SYNONYMS = getattr(settings, 'BLOG_CUT_TAG_SYNONYMS', ['<!--more-->'])
ENABLE_USER_BLOG = getattr(settings, 'BLOG_ENABLE_USER_BLOG', True)
ENABLE_BLOGS = getattr(settings, 'BLOG_ENABLE_BLOGS', True)
