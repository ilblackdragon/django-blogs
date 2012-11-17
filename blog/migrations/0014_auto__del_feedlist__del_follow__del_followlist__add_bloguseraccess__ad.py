# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'FeedList'
        db.delete_table('blog_feedlist')

        # Removing M2M table for field posts on 'FeedList'
        db.delete_table('blog_feedlist_posts')

        # Deleting model 'Follow'
        db.delete_table('blog_follow')

        # Deleting model 'FollowList'
        db.delete_table('blog_followlist')

        # Removing M2M table for field follows on 'FollowList'
        db.delete_table('blog_followlist_follows')

        # Adding model 'BlogUserAccess'
        db.create_table('blog_bloguseraccess', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Blog'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('is_moderator', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_write', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('blog', ['BlogUserAccess'])

        # Adding field 'Blog.opened_blog'
        db.add_column('blog_blog', 'opened_blog', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'FeedList'
        db.create_table('blog_feedlist', (
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='feed_list_owner', to=orm['auth.User'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('blog', ['FeedList'])

        # Adding M2M table for field posts on 'FeedList'
        db.create_table('blog_feedlist_posts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feedlist', models.ForeignKey(orm['blog.feedlist'], null=False)),
            ('post', models.ForeignKey(orm['blog.post'], null=False))
        ))
        db.create_unique('blog_feedlist_posts', ['feedlist_id', 'post_id'])

        # Adding model 'Follow'
        db.create_table('blog_follow', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blog', self.gf('django.db.models.fields.related.ForeignKey')(related_name='follow_blog', null=True, to=orm['blog.Blog'], blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='follow_user', null=True, to=orm['auth.User'], blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='follow_owner', to=orm['auth.User'])),
            ('follow_list', self.gf('django.db.models.fields.related.ForeignKey')(related_name='follow_list', null=True, to=orm['blog.FollowList'], blank=True)),
        ))
        db.send_create_signal('blog', ['Follow'])

        # Adding model 'FollowList'
        db.create_table('blog_followlist', (
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='follow_list_owner', to=orm['auth.User'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('blog', ['FollowList'])

        # Adding M2M table for field follows on 'FollowList'
        db.create_table('blog_followlist_follows', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('followlist', models.ForeignKey(orm['blog.followlist'], null=False)),
            ('follow', models.ForeignKey(orm['blog.follow'], null=False))
        ))
        db.create_unique('blog_followlist_follows', ['followlist_id', 'follow_id'])

        # Deleting model 'BlogUserAccess'
        db.delete_table('blog_bloguseraccess')

        # Deleting field 'Blog.opened_blog'
        db.delete_column('blog_blog', 'opened_blog')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'blog.blog': {
            'Meta': {'object_name': 'Blog'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '256', 'blank': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'default': "'blog_icons/default.jpg'", 'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'opened_blog': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'user_access_list': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'blog_user_access_list'", 'symmetrical': 'False', 'through': "orm['blog.BlogUserAccess']", 'to': "orm['auth.User']"})
        },
        'blog.bloguseraccess': {
            'Meta': {'object_name': 'BlogUserAccess'},
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.Blog']"}),
            'can_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_write': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_moderator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'blog.post': {
            'Meta': {'ordering': "('-updated_at',)", 'object_name': 'Post'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'added_posts'", 'to': "orm['auth.User']"}),
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'post_list'", 'null': 'True', 'to': "orm['blog.Blog']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'creator_ip': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_comment_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'publish': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'tease': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ratings.score': {
            'Meta': {'unique_together': "(('content_type', 'object_id'),)", 'object_name': 'Score'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['blog']
