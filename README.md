# PyScene

PyScene is a custom python + pygame framework / engine developed to streamline 2d game development.
This is not a pygame wrapper, as it goed beyons the basic helper features and dives into a mini engine / framework.

Please Note: This engine is still in development and many features, like tilemaps and audio, are a work in progress. It also lack any form of documentation, I ask for patience as docs will be rolled out once the core features are more solidified.

PyScene is in developement and API's may change offten, a fully stable version should come with v2.0.0, currently on v1.1.3

Getting Started Basics:

1. Use Game.init(...)
2. Create custom Game Objects by inheriting GameObj
3. Create a Scene by inheriting Scene
4. Use Game.Run(...) #pass in True to have escape close the window
Not: remenber to use super().__init__(...) is any inherited scene or Game object
