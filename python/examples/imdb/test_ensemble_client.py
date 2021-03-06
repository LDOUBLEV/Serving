# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# pylint: disable=doc-string-missing

from paddle_serving_client import Client
from imdb_reader import IMDBDataset

client = Client()
# If you have more than one model, make sure that the input
# and output of more than one model are the same.
client.load_client_config('imdb_bow_client_conf/serving_client_conf.prototxt')
client.connect(["127.0.0.1:9393"])

# you can define any english sentence or dataset here
# This example reuses imdb reader in training, you
# can define your own data preprocessing easily.
imdb_dataset = IMDBDataset()
imdb_dataset.load_resource('imdb.vocab')

for i in range(3):
    line = 'i am very sad | 0'
    word_ids, label = imdb_dataset.get_words_and_label(line)
    feed = {"words": word_ids}
    fetch = ["acc", "cost", "prediction"]
    fetch_maps = client.predict(feed=feed, fetch=fetch)
    if len(fetch_maps) == 1:
        print("step: {}, res: {}".format(i, fetch_maps['prediction'][0][1]))
    else:
        for model, fetch_map in fetch_maps.items():
            print("step: {}, model: {}, res: {}".format(i, model, fetch_map[
                'prediction'][0][1]))
