# CLion Project Template

1. Copy paste this directory, i.e. `clion_project_template` to where you would like your project to live. This must be outside of the repository and somewhere in your user's home directory. For example `~/Development/rai-cpp-dev`.
2. Create symlinks of all repos into `~/Development/<MY_PROJECT>/src` (or just clone them directly if you prefer).
3. Open CLion, choose `Open Project`, and select `~/Development/<MY_PROJECT>/src/CMakeLists.txt`.

You can modify this project to add more packages and build it all in CLion. Do not expect it however to work out-of-the-box once modified. You will have to ensure that all headers and libraries are exported correctly.
