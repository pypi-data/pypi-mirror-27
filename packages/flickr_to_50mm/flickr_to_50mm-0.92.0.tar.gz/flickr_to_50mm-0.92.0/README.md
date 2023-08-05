# Flickr to 50mm Configuration Generator

`flickr_to_50mm` is a tool built to help you move your photo albums from flickr to [50mm](https://github.com/agile-leaf/50mm) (self-hosted and simple photo gallery software) - the catch is that it doesn't transfer any photos for you, only ordering configuration so that you don't have to re-do all that hard work.

For exporting your actual photos from flickr I can recommend [flickrtouchr](https://github.com/dan/hivelogic-flickrtouchr), it's a little rough around the edges but it works.

### Installation

Currently, `git clone` this repository, `pip install -r requirements.txt` and then run as below. virtualenvs are recommended.

### Usage

1. Get yourself an API key from flickr from here: https://www.flickr.com/services/apps/create/apply/
1. Find your user ID, this is often in your album URLS, you'll see it in links like: `https://www.flickr.com/photos/<YOUR_ID_IS_HERE>/albums`
1. `python flickr_to_50mm.py THAT_API_KEY_FROM_STEP_1 THAT_USER_ID_FROM_STEP_2`
1. You should get a yaml file dumped for each album on flickr

### Known limitations

 - Pretty sure things go wonky if an album has more than 500 photos (due to pagination), PRs welcome to account for that since I don't have any albums to practice on.
 - We don't do much status code checking or rate limit checking, the assumption is that everything is always perfect... I mean, this is not production software.
 - All or nothing processed - there is no ability to specify albums, if there's popular demand it's actually easy to implement, will do, just open an issue.

### Unknown Limitations

 - This was smacked together real quick for personal use, I'm pretty sure there will be 10,000 edge cases I've not accounted for, if you find one and it's easy to fix, please submit a PR.
