In this document we'll walk through 2 examples, one is the php default build, which can be sufficient for some, but it's advisable to compile only what you need. I find it benefitial in multiple fronts.

so, let's start with the default

pvm install 8.4.8

pvm use 8.4.8


### Dual versions

pvm install 8.3.22

pvm use 8.3.22

switching is as easy as you see using the use command

### Persisting a certain version to be the default

```
echo 'eval "$(pvm use 8.3.22)"' >> ~/.zshrc

or

echo 'eval "$(pvm use 8.3.22)"' >> ~/.bashrc
```
