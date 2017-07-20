'use strict';

module.exports = function (grunt) {
    grunt.initConfig({
        watch: {
            styles: {
                files: [
                    'assets/styles/**/*.less',
                ],
                tasks: ['styles'],
            },
            main: {
                files: [
                    'assets/scripts/**/*.js',
                ],
                tasks: ['uglify:main',  'jscs',],
            },
            bower_components: {
                files: [
                    'bower_components/**/*'
                ],
                tasks: ['all'],
            },
            python: {
                files: [
                    'bikeanjo.py',
                ],
                tasks: ['flake8',],
            },
        },
        uglify: {
            options: {
                sourceMap: true,
                sourceMapIncludeSources: true,
                compress: {
                    drop_console: false
                },
            },
            vendor: {
                files: {
                    'static/js/vendor.js': [
                        'bower_components/jquery/dist/jquery.js',
                        'bower_components/bootstrap/dist/js/bootstrap.js',
                        'bower_components/leaflet/dist/leaflet.js',
                        'bower_components/sprintf/dist/sprintf.min.js',
                        'bower_components/bootstrap-switch/dist/js/bootstrap-switch.js',
                    ],
                },
            },
            vendor_admin: {
                files: {
                    'static/js/vendor_admin.js': [
                        'bower_components/jquery.browser/dist/jquery.browser.js'
                    ],
                },
            },
            main: {
                files: {
                    'static/js/main.js': [
                        'assets/scripts/**/*.js',
                    ],
                },
            },
        },
        less: {
            options: {
                compress: true,
                sourceMap: true,
                outputSourceFiles: true,
            },
            app: {
                options: {
                    sourceMapFilename: 'main.css.map',
                },
                files: {
                    'static/css/main.css': [
                        'assets/styles/main.less',
                    ],
                    'static/css/admin.css': [
                        'assets/styles/admin.less',
                    ],
                },
            },
        },
        rename: {
            csssourcemap: {
                src: 'main.css.map',
                dest: 'static/css/',
            },
        },
        copy: {
            assets: {
                files: [
                    {expand: true, cwd: 'assets/data', src:['**'], dest: 'static/data/', },
                    {expand: true, cwd: 'assets/imgs', src:['**'], dest: 'static/imgs/', },
                    {expand: true, cwd: 'assets/fonts', src:['**'], dest: 'static/fonts/', },
                    {expand: true, cwd: 'assets/fonts', src:['**'], dest: 'static/fonts/', },
                ],
            },
            leaflet: {
                files:[
                    {expand: true, cwd: 'bower_components/leaflet/dist/images', src:['**'], dest: 'static/imgs/', },
                    {expand: true, flatten: true, src: ['bower_components/leaflet/dist/leaflet.css'], dest: 'static/css/',},
                ],
            },
            fontawesome: {
                files: [
                    {expand: true, flatten: true, src: ['bower_components/font-awesome/fonts/*'], dest: 'static/fonts/', filter: 'isFile',},
                    {expand: true, flatten: true, src: ['bower_components/font-awesome/css/*.css'], dest: 'static/css/', filter: 'isFile',},
                    {expand: true, flatten: true, src: ['bower_components/fontawesome/fonts/fontawesome-webfont.woff2'], dest: 'static/fonts/'},
                ],
            },
        },
        jshint: {
            options: {
                reporter: require('jshint-stylish'),
                globals: {
                    jQuery: true,
                },
                force: true,
            },
            all: [
                ['assets/scripts/**/*.js', '!assets/scripts/vendor/**/*.js'],
            ],
        },
        jscs: {
            src: ['assets/scripts/**/*.js', '!assets/scripts/vendor/**/*.js'],
            options: {
                requireCurlyBraces: ['if', ],
                force: true,
                disallowMixedSpacesAndTabs: true,
            },
        },
        flake8: {
            options: {
                force: true,
                errorsOnly: true,
                maxLineLength: 250,
            },
            src: ['manage.py', ],
        },
        browserSync: {
            options: {
                watchTask: true, // < VERY important
            },
            app: {
                bsFiles: {
                    src : [
                        'static/css/*.css',
                        'static/js/*.js',
                        'templates/*.html',
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
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-jscs');
    grunt.loadNpmTasks('grunt-flake8');
    grunt.loadNpmTasks('grunt-browser-sync');

    // define default task
    grunt.registerTask('styles', ['less', 'rename',]);
    grunt.registerTask('all', ['uglify', 'jscs', 'flake8', 'styles', 'copy',])
    grunt.registerTask('default', ['all', 'browserSync', 'watch',]);
};
