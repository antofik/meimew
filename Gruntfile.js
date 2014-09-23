module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    uglify: {
      options: {
      },
      build: {
        src: [
			'media/plugins/jquery-1.11.1.min.js',
			'media/plugins/bootstrap-3.2.0/js/bootstrap.min.js',
			'media/plugins/jquery.ui.widget.js',
			'media/plugins/jquery.fileupload.js',
			'media/plugins/jquery.iframe-transport.js',
			'media/plugins/jquery.fileupload-process.js',
			'media/plugins/ZeroClipboard.min.js'
		],
        dest: 'media/js/main.min.js'
      }
    },
	cssmin: {
		combine: {
			files: {
				'media/css/main.css': [
					'media/plugins/bootstrap-3.2.0/css/bootstrap.min.css',
					'media/plugins/jquery.fileupload.css',
					'media/plugins/jquery.fileupload-ui.css'
				]
			}
		}
	},
	uncss: {
		dist: {
			options: {
				csspath: '../',
				stylesheets: ['media/css/main.css'],
                report: 'min'
			},
			files: {
				'media/css/main.min.css': ['templates/home.html']
			}
		}
	},	
	copy: { 
		main:{
			files: [
			{
				expand: true,
				flatten: true,
				cwd: 'media/plugins/',
				src: ['ZeroClipboard.swf'], 
				dest: 'media/js/'
			},		
			{
				expand: true,
				flatten: true,
				cwd: 'media/plugins/bootstrap-3.2.0/fonts/',
				src: ['*.*'], 
				dest: 'media/fonts/'
			},
		]}
	}	
	
  });

  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-uncss');

  grunt.registerTask('default', ['uglify', 'cssmin', 'copy', 'uncss']);

};