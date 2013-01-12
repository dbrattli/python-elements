from elements import Element, TextElement, TextAttribute, DateTimeElement

ATOM_NAMESPACE = 'http://www.w3.org/2005/Atom'
APP_NAMESPACE = 'http://www.w3.org/2007/app'

class Link(Element):
    """The atom:link element"""

    _tag = 'link'
    _namespace = ATOM_NAMESPACE
    
    rel = TextAttribute()
    href = TextAttribute()
    type = TextAttribute()
    title = TextAttribute()
    length = TextAttribute()
    hreflang = TextAttribute()

class Person(Element):
    """A foundation class from which atom:author and atom:contributor extend.

    A person contains information like name, email address, and web page URI for
    an author or contributor to an Atom feed. 
    """
    _namespace = ATOM_NAMESPACE
    
    name = TextElement()
    email = TextElement()
    uri = TextElement()

class Contributor(Person):
    """The atom:contributor element"""

    _tag = 'contributor'
    _namespace = ATOM_NAMESPACE

class Author(Person):
    """The atom:author element
    
    An author is a required element in Feed. 
    """
    _tag = 'author'
    _namespace = ATOM_NAMESPACE

class Text(Element):
  """A foundation class from which atom:title, summary, etc. extend.
  
  This class should never be instantiated.
  """

  type = TextAttribute()

class Title(Text):
    """The atom:title element"""

    _tag = 'title'
    _namespace = ATOM_NAMESPACE

class Subtitle(Text):
    """The atom:subtitle element"""

    _tag = 'subtitle'
    _namespace = ATOM_NAMESPACE

class Rights(Text):
    """The atom:rights element"""

    _tag = 'rights'
    _namespace = ATOM_NAMESPACE

class Summary(Text):
    """The atom:summary element"""

    _tag = 'summary'
    _namespace = ATOM_NAMESPACE

class Content(Text):
    """The atom:content element"""

    _tag = 'content'
    _namespace = ATOM_NAMESPACE

    src = TextAttribute()

class Generator(Element):
    """The atom:generator element"""

    _tag = 'generator'
    _namespace = ATOM_NAMESPACE

    uri = TextAttribute()
    version = TextAttribute()

class Category(Element): 
    """The atom:category element"""
                      
    _tag = 'category'
    _namespace = ATOM_NAMESPACE
    
    term = TextAttribute()
    scheme = TextAttribute()
    label = TextAttribute()

class Control(Element):
    """The app:control element indicating restrictions on publication.

    The APP control element may contain a draft element indicating whether or
    not this entry should be publicly available.
    """

    _tag = 'control'
    _namespace = APP_NAMESPACE

    draft = TextElement()

class FeedEntryParent(Element):
    """A super class for atom:feed and entry, contains shared attributes"""
    
    author = Author()
    category = Category()
    contributor = Contributor()
    id = TextElement()
    link = Link()
    rights = Rights()
    title = Title()
    updated = DateTimeElement(format='%Y-%m-%dT%H:%M:%SZ')

class Source(FeedEntryParent):
    """The atom:source element"""

    _tag = 'source'
    _namespace = ATOM_NAMESPACE

    generator = Generator()
    icon = TextElement()
    logo = TextElement()
    subtitle = Subtitle()

class Entry(FeedEntryParent):
    """The atom:entry element"""

    _tag = 'entry'
    _namespace = ATOM_NAMESPACE
    
    content = Content()
    published = TextElement()
    source = Source()
    summary = Summary()
    control = Control()
    
class Feed(Source):
    """The atom:feed element"""

    _tag = 'feed'
    _namespace = ATOM_NAMESPACE
    
    entry = Entry()
    
if __name__ == '__main__':
    feed = Feed()
    feed.from_file("atom.xml")
    #print feed
    
    print "1*****************************************"
    print feed['title']
    print "2*****************************************"
    print feed.entry
    print "3*****************************************"
    print feed.entry[0]
    print "4*****************************************"
    print feed.entry.title
    print "5*****************************************"
    print feed.entry.control.draft
    print "#####################"
    feed.entry.control.draft = "Testing"
    print "#####################"    
    print feed.entry.control.draft
    print feed.to_string()