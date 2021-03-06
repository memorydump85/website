/*
 *  Copyright 2006 - 2010 by Jens Boje
 *  Name    : Imago Loaders
 *  Version : 0.8
 *  Author  : Jens Boje (azarai@codeboje.de)
 *  URL		: http://codeboje.de
 *  Terms of Use:
 *			 Imago may be used in any kinds of personal and/or commercial projects.
 *			 Redistribution or reselling to other companies or third parties is prohibited.
 *			 Specifically, no Redistribution as part of a content management system or online hosting solution.
 */

var SmugmugLoader=new Class({Extends:GalleryLoader,initialize:function(albumId,showCaptions){this.albumId=albumId;this.showCaptions=showCaptions},specialLoading:function(){new MooSmug().callSmugmug({method:'smugmug.login.anonymously'});jsonSmugmugApi=function(rsp){if(rsp.stat=='ok'){if(rsp.Login){gallery.loader.sessionId=rsp.Login.Session.id;new MooSmug().callSmugmug({method:'smugmug.albums.getInfo',AlbumID:gallery.loader.albumId,SessionID:gallery.loader.sessionId})}else if(rsp.Album){gallery.title=rsp.Album.Title;new MooSmug().callSmugmug({method:'smugmug.images.get',AlbumID:gallery.loader.albumId,Heavy:gallery.loader.showCaptions,SessionID:gallery.loader.sessionId})}else if(rsp.Images){for(var i=0;i<rsp.Images.length;i++){var url='http://smugmug.com/photos/'+rsp.Images[i].id;var caption="";if(gallery.loader.showCaptions){caption=rsp.Images[i].Caption}gallery.addImage(new GalleryImage(rsp.Images[i].id,caption,url+'-75x75.jpg',url+'-M.jpg'))}gallery.loader.finished()}}else{gallery.loader.error("Can't load photos from smugmug")}}}});