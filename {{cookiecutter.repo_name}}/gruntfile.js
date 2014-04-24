module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    watch: {
      options: {
        livereload: true,
      },

      compass: {
        files: ['src/css/**/*.scss'],
        tasks: ['compass:server']
      },

      cssmin: {
        files: ['<%= pkg.name %>/static/css/project.css'],
        tasks: ['cssmin']
      },

      scripts: {
        files: ['src/js/**/*.js'],
        tasks: ['concat', 'uglify']
      },

      images: {
        files: ['src/img/**/*'],
        tasks: ['imagemin']
      },

      grunticon: {
        files: ['src/icons/*'],
        tasks: ['grunticon']
      },

      template: {
        files: '<%= pkg.name %>/templates/**/*'
      },

      views: {
        files: '<%= pkg.name %>/**/views.py'
      }
    },

    compass: {
      options: {
        sassDir: 'src/css',
        cssDir: '<%= pkg.name %>/static/css',
        environment: 'development'
      },

      server: {
        options: {
          debugInfo: false
        }
      }
    },

    concat: {
      project: {
        src: ['src/js/project/jquery.js', 'src/js/project/includes/**/*.js'],
        dest: '<%= pkg.name %>/static/js/project.js'
      },

      project_init: {
        src: ['src/js/project_init/**/*.js'],
        dest: '<%= pkg.name %>/static/js/project_init.js'
      }
    },

    cssmin: {
      minify: {
        src: ['<%= pkg.name %>/static/css/project.css'],
        dest: '<%= pkg.name %>/static/css/project.min.css'
      }
    },

    uglify: {
      dist: {
        files: {
          '<%= pkg.name %>/static/js/project.min.js': ['<%= pkg.name %>/static/js/project.js'],
          '<%= pkg.name %>/static/js/project_init.min.js': ['<%= pkg.name %>/static/js/project_init.js'],
        }
      },
    },

    imagemin: {
      static: {
        files: [{
          expand: true,
          cwd: 'src/img/',
          src: ['**/*.{png,jpg,gif}'],
          dest: '<%= pkg.name %>/static/img/'
        }]
      }
    },

    grunticon: {
      theme: {
        options: {
          src: "src/icons",
          dest: "<%= pkg.name %>/static/icons",
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-compass');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-imagemin');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-grunticon');

  grunt.registerTask('server', function (target) {
    if (target === 'dist') {
      return grunt.task.run(['build', 'open', 'connect:dist:keepalive']);
    }

    grunt.task.run([
      'watch'
      ]);
  });

};