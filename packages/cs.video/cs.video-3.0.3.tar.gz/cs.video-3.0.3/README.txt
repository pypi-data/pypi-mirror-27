Introduction
=============

cs.video provides a Video object to refere to externally hosted FLV files. It uses FlowPlayer to show the video in the Plone site.

It also provides to additional views for Folder and Large Folders to show current folder's videos and also a video archive to show videos on folders inside current folder.

We are using this at https://dantzan.eus/bideoak

In its template the video is shown using FlowPlayer, which is included and distributed with the product.

A macro called player is defined in the video_view template to be able to reuse the player in other templates such as portlets


- Code repository: https://github.com/codesyntax/cs.video

