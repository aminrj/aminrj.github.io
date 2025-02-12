# Improving my note taking workflow

Why I switched from Notion and Vimwiki to NeoVim and Obsidian ?

And this is not about a tool switch, it made all the difference.
From taking notes from time to time (1 or 2 per week), to doing it all the time.

In this post, I want to explain why I moved from using VimWiki and Notion for my
note-taking and journaling.

Note taking is a big part of my daily habits.
I appreciate the process of putting my thought in writing and clear my mind.
I read several studies/books/blogs that details the many benefits of such habit.

## Vim for private notes and journals

So, for the last decade or so, I was using VimWiki for private journaling.
I put together a small script that encrypt the content of my journal.
Then, the encrypted file is stored in Dropbox to be synced on my other devices
and for safe storage on the Internet.

Although this was working fine for me, there was some drawbacks:

- It was cumbersome to have to do the sync manually: Each time I want to save my
  journal and create backups, I need to run my script manually from my laptop.
- After a decade worth of notes and journal entries, my script, even if it is
  simple and short, it start to take some seconds to run.
- The main drawback is that I couldn't access my notes on the go from my mobile.
  Nor I could take notes from my mobile (the same way I did on my laptop).

## Notion for less sensitive notes and better access

Then, for notes that I am comfortable sharing on a public platform
-aka, a platform that I don't trust-, I used Notion.
Notion is a good candidate to just start taking notes and having them synced
with my mobile.

I was using it mainly for managing projects, track progress and keep
related information at hands reach.

Notion solved the access limitation of VimWiki but I was "trusting" the privacy of
my notes to a third party company.
Little to say is that I wasn't comfortable with that.
So, my note-taking habit on Notion never took off.

For all these reasons, and after all this time using the same tools, I started
to look around for new and improved workflow for note-taking and journaling.

## NeoVim for better note-taking experience

While searching for what's out there to take notes, I found NeoVim.
I knew that NeoVim is mainly another flavor of Vim, but never went beyond that.

But, this time, I gave a chance and started exploring the key differences.

I was gladly surprised by philosophy behind it (better community) and the
convenience of using plugins that took my Vim experience to another level.

## MarkDown everywhere

Also, using MarkDown instead of VimWiki was another positive switch.

MarkDown is THE format of content on the Internet nowadays and I was already
using it for my blogs and websites.

Now, I am also using it for my notes which is another plus.

## This led me to Obsidian for online access

Yes, Obsidian is yet another online note taking tool.

However, contrary to Notion, all the notes are stored in MarkDown files and can
be kept private on you local machine.
Which is not a small deal in my particular use case.

For inter-device sync, one can choose their paid solution to enable end-to-end
encryption.
Basically, what I was using my own script for with VimWiki, but more automated.

For now, I am putting my Vault (Obsidian term for the root folder of
you notes) in my iCloud storage.

I know that this is not as private as my own storage and encryption, but for
now, I can live with it knowing that Apple has far more private data on me.😳

## Enough story-telling and let's see how it works

Here are my criteria when I decided to switch my note-taking process:

- [x] Easy way to write notes
- [x] Fast way to organise them for quick reference/read
- [x] Available everywhere

### Zettelkasten approach

I read about the Zettelkasten methodology and I like the idea of having
my notes linked to each other to build a connected chain of thoughts.

This is what Obsidian offer to do with my notes.

### Building my "second-brain"

I also read a Book on Building a second-brain by actively and continuously
taking notes and organizing them into the PARA structure (Projects, Areas,
Resources, Archive).

However, It never took off because I didn't get back to my notes often.

Also, I didn't like taking active effort to organize notes into these
categories with little added value.
I addition, I didn't have a quick and easy way of searching through them.

So, my PARA implementation on Notion wasn't very useful over time.

### NeoVim plugins to the rescue

I installed some new plugins that improved my experience using Vim.
Now, I am using Vim for all my writing and coding activities.

By far, the most important one is the fuzzy searching among all my files/notes.
Now, my notes are more than just for journaling that I seldom check after I
wrote them.
They are easily and rapidly searchable and available.

Now, I am building my second-brain and I think that it is rather useful.

Here is my setup:

1. NeoVim for taking notes and searching through them: NeoVim is now where I
   spend most of my time writing notes, content, journals, code...
2. Obsidian for note syncing and mobile access
3. Git for versioning and coding (however, I don't push my notes anywhere. Yet)

## Plans for the future

I am planning on saving a copy of my notes (Vault) on a private Git server.
I am waiting on my HomeLab deployed Git tool to start pushing my commits.
I consider my notes and journals are too sensitive to trust a public Git
company get them.
Even if the repo is configured to be private.
