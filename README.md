# conan-angelscript
Conan recipe for Angelscript

# How to test

To test this recipe, you need to create it:
`conan create . angelscript/2.34.0@noizex/testing`

This also takes parameters for the build - for example if you want to test Debug build you can run:
`conan create . angelscript/2.34.0@noizex/testing -s build_type=Debug`

