# mezzanine-recipes

This plugin gives you a "Recipe" page type for your Mezzanine sites.

## Features

* Show your visitors what to cook
	* Embed an image of the meal
	* Provide an ingredient list
* Let your visitors add a comment to recipes
* The usual stuff - ingredients, times, categories
* REST-API for external applications

## Installation

* Run `pip install https://github.com/tjetzinger/mezzanine-recipes/tarball/master` (or, if you want to hack on mezzanine-recipes, clone it and run `pip install -e path/to/repo`)
* Add `"mezzanine_recipes"` to your `INSTALLED_APPS`
* Migrate your database

## Usage

mezzanine-recipe provides the page type "Recipe". It is the 'Recipe' page on your website. The Recipe page type represents a single recipe.

Create an Recipe page in the Mezzanine admin (naming it something like "Recipe").

## Creating Templates

### Recipe page

The template for an Recipe page is `templates/pages/recipe.html`.

The Recipe object is available at `page.recipe`. It has the following properties:

* Periods and times: `WorkingHours`, `CookingTime`, `RestPeriod`
* Cooking info: `ingredients`, `portions`, `difficulty`, `categories`
* Text data: `title`, `summary`, `content`, `comments`

## To Do

* Create a clean recipe template
* Let visitors add a rating to recipes
* Extend the REST API for comment fields
* Add some tests

## License

Copyright (C) 2012 Thomas Jetzinger

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.