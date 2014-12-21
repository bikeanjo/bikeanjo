'use strict';

module.exports = function (grunt) {
    grunt.initConfig({
        watch: {
            files: [
                'static/less/**/*.less',
                'bower_components/**/*'
            ],
            tasks: ['styles'],
        },
        uglify: {
            options: {
                sourceMap: true,
                sourceMapIncludeSources: true,
                compress: true,
            },
            vendor: {
                files: {
                    'static/js/vendor.js': [
                        'bower_components/jquery/dist/jquery.js',
                        'bower_components/bootstrap/dist/js/bootstrap.js'
                    ],
                },
            },
        },
        less: {
            options: {
                paths: ['assets/css'],
                compress: true,
                sourceMap: true,
                outputSourceFiles: true,
            },
            app: {
                options: {
                    sourceMapFilename: 'main.css.map',
                },
                files: {
                    'static/css/main.css': 'static/less/main.less',
                },
            },
        },
        rename: {
            csssourcemap: {
                src: 'main.css.map',
                dest: 'static/css/',
            },
        },
        browserSync: {
            options: {
                watchTask: true // < VERY important
            },
            app: {
                bsFiles: {
                    src : [
                        'static/css/*.css',
                        'static/js/*.js',
                        'templates/*.html'
                    ]
                },
            },
        },
    });

    // load npm tasks
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-rename');
    grunt.loadNpmTasks('grunt-browser-sync');

    // define default task
    grunt.registerTask('styles', ['less', 'rename']);
    grunt.registerTask('scripts', ['uglify']);
    grunt.registerTask('default', ['scripts', 'styles', 'browserSync', 'watch']);
};
