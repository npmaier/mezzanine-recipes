# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Recipe'
        db.create_table('mezzanine_recipes_recipe', (
            ('page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pages.Page'], unique=True, primary_key=True)),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recipes', to=orm['auth.User'])),
            ('cover', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('portions', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('difficulty', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('allow_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('mezzanine_recipes', ['Recipe'])

        # Adding M2M table for field categories on 'Recipe'
        db.create_table('mezzanine_recipes_recipe_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recipe', models.ForeignKey(orm['mezzanine_recipes.recipe'], null=False)),
            ('recipecategory', models.ForeignKey(orm['mezzanine_recipes.recipecategory'], null=False))
        ))
        db.create_unique('mezzanine_recipes_recipe_categories', ['recipe_id', 'recipecategory_id'])

        # Adding model 'RecipeCategory'
        db.create_table('mezzanine_recipes_recipecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
        ))
        db.send_create_signal('mezzanine_recipes', ['RecipeCategory'])

        # Adding model 'Ingredient'
        db.create_table('mezzanine_recipes_ingredient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mezzanine_recipes.Recipe'])),
            ('quantity', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('unit', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ingredient', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('mezzanine_recipes', ['Ingredient'])

        # Adding model 'WorkingHours'
        db.create_table('mezzanine_recipes_workinghours', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hours', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('minutes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('recipe', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mezzanine_recipes.Recipe'], unique=True)),
        ))
        db.send_create_signal('mezzanine_recipes', ['WorkingHours'])

        # Adding model 'CookingTime'
        db.create_table('mezzanine_recipes_cookingtime', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hours', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('minutes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('recipe', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mezzanine_recipes.Recipe'], unique=True)),
        ))
        db.send_create_signal('mezzanine_recipes', ['CookingTime'])

        # Adding model 'RestPeriod'
        db.create_table('mezzanine_recipes_restperiod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hours', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('minutes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('recipe', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mezzanine_recipes.Recipe'], unique=True)),
            ('days', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('mezzanine_recipes', ['RestPeriod'])


    def backwards(self, orm):
        # Deleting model 'Recipe'
        db.delete_table('mezzanine_recipes_recipe')

        # Removing M2M table for field categories on 'Recipe'
        db.delete_table('mezzanine_recipes_recipe_categories')

        # Deleting model 'RecipeCategory'
        db.delete_table('mezzanine_recipes_recipecategory')

        # Deleting model 'Ingredient'
        db.delete_table('mezzanine_recipes_ingredient')

        # Deleting model 'WorkingHours'
        db.delete_table('mezzanine_recipes_workinghours')

        # Deleting model 'CookingTime'
        db.delete_table('mezzanine_recipes_cookingtime')

        # Deleting model 'RestPeriod'
        db.delete_table('mezzanine_recipes_restperiod')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'generic.assignedkeyword': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'AssignedKeyword'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': "orm['generic.Keyword']"}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {})
        },
        'generic.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'mezzanine_recipes.cookingtime': {
            'Meta': {'object_name': 'CookingTime'},
            'hours': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minutes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'recipe': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mezzanine_recipes.Recipe']", 'unique': 'True'})
        },
        'mezzanine_recipes.ingredient': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Ingredient'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mezzanine_recipes.Recipe']"}),
            'unit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'mezzanine_recipes.recipe': {
            'Meta': {'ordering': "('-publish_date',)", 'object_name': 'Recipe', '_ormbases': ['pages.Page']},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'recipes'", 'blank': 'True', 'to': "orm['mezzanine_recipes.RecipeCategory']"}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'cover': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'difficulty': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['pages.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'portions': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recipes'", 'to': "orm['auth.User']"})
        },
        'mezzanine_recipes.recipecategory': {
            'Meta': {'object_name': 'RecipeCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'mezzanine_recipes.restperiod': {
            'Meta': {'object_name': 'RestPeriod'},
            'days': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hours': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minutes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'recipe': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mezzanine_recipes.Recipe']", 'unique': 'True'})
        },
        'mezzanine_recipes.workinghours': {
            'Meta': {'object_name': 'WorkingHours'},
            'hours': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minutes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'recipe': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mezzanine_recipes.Recipe']", 'unique': 'True'})
        },
        'pages.page': {
            'Meta': {'ordering': "('titles',)", 'object_name': 'Page'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'content_model': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_menus': ('mezzanine.pages.fields.MenusField', [], {'default': '[1, 2, 3]', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': "orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['pages.Page']"}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'titles': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['mezzanine_recipes']