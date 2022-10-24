@ECHO OFF

pushd %~dp0

git push --all
git push --all aivclab
git push --tags aivclab

popd
