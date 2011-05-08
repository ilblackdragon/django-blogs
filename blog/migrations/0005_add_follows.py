
from south.db import db
from django.db import models
from blog.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Follow'
        db.create_table('blog_follow', (
            ('id', orm['blog.follow:id']),
            ('owner', orm['blog.follow:owner']),
            ('user', orm['blog.follow:user']),
            ('category', orm['blog.follow:category']),
            ('follow_list', orm['blog.follow:follow_list']),
        ))
        db.send_create_signal('blog', ['Follow'])
        
        # Adding model 'FeedList'
        db.create_table('blog_feedlist', (
            ('id', orm['blog.feedlist:id']),
            ('owner', orm['blog.feedlist:owner']),
        ))
        db.send_create_signal('blog', ['FeedList'])
        
        # Adding model 'FollowList'
        db.create_table('blog_followlist', (
            ('id', orm['blog.followlist:id']),
            ('owner', orm['blog.followlist:owner']),
            ('slug', orm['blog.followlist:slug']),
        ))
        db.send_create_signal('blog', ['FollowList'])
        
        # Adding ManyToManyField 'FollowList.follows'
        db.create_table('blog_followlist_follows', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('followlist', models.ForeignKey(orm.FollowList, null=False)),
            ('follow', models.ForeignKey(orm.Follow, null=False))
        ))
        
        # Adding ManyToManyField 'FeedList.posts'
        db.create_table('blog_feedlist_posts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feedlist', models.ForeignKey(orm.FeedList, null=False)),
            ('post', models.ForeignKey(orm.Post, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Follow'
        db.delete_table('blog_follow')
        
        # Deleting model 'FeedList'
        db.delete_table('blog_feedlist')
        
        # Deleting model 'FollowList'
        db.delete_table('blog_followlist')
        
        # Dropping ManyToManyField 'FollowList.follows'
        db.delete_table('blog_followlist_follows')
        
        # Dropping ManyToManyField 'FeedList.posts'
        db.delete_table('blog_feedlist_posts')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'blog.category': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'blog.feedlist': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feed_list_owner'", 'to': "orm['auth.User']"}),
            'posts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['blog.Post']"})
        },
        'blog.follow': {
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'follow_category'", 'null': 'True', 'to': "orm['blog.Category']"}),
            'follow_list': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'follow_list'", 'null': 'True', 'to': "orm['blog.FollowList']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'follow_owner'", 'to': "orm['auth.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'follow_user'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'blog.followlist': {
            'follows': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['blog.Follow']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'follow_list_owner'", 'to': "orm['auth.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'blog.post': {
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'added_posts'", 'to': "orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'post_list'", 'null': 'True', 'to': "orm['blog.Category']"}),
            'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'creator_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_comment_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'publish': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'tease': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['blog']
