import asyncio
import unittest
from unittest import mock

from aiohttp import ClientSession

from tests.utils import AsyncMeta, fake_response as f_resp
from lapka import fetch


all_animals = '''
<div class="content">
  <div class="filter-area" style="margin-top: -41px;">
    <div class="bootstrap-3">
      <!-- bootstrap 3 -->
      <div class="container">
        <div class="row" data-tesla-plugin="masonry" style="position: relative; height: 4032.63px;">
          <div class="col-sm-4 col-xs-6 psy psy-male" style="position: absolute; left: 0px; top: 0px;">
            <div class="filter-item">
              <div class="filter-hidden">
                <div class="filter-hover">
                  <h5><a href="http://schroniskowroclaw.pl/displaywp_project/burbon-22117/">Burbon (221/17)</a></h5>
                  <ul>
                    <li><a class="filter-zoom swipebox everlightbox-trigger" href="http://schroniskowroclaw.pl/wp-content/uploads/2017/03/burbon2.jpg"></a></li>
                    <li><a class="filter-link" href="http://schroniskowroclaw.pl/displaywp_project/burbon-22117/"></a></li>
                  </ul>
                </div>
                <div class="filter-cover">
                  <img src="http://schroniskowroclaw.pl/wp-content/uploads/2017/03/burbon2.jpg" alt="project">
                </div>
              </div>
            </div>
          </div>
          <div class="col-sm-4 col-xs-6 koty" style="position: absolute; left: 390px; top: 0px;">
            <div class="filter-item">
              <div class="filter-hidden">
                <div class="filter-hover">
                  <h5><a href="http://schroniskowroclaw.pl/displaywp_project/nelson-10117/">Nelson (101/17)</a></h5>
                  <ul>
                    <li><a class="filter-zoom swipebox everlightbox-trigger" href="http://schroniskowroclaw.pl/wp-content/uploads/2017/02/DSCF9112.jpg"></a></li>
                    <li><a class="filter-link" href="http://schroniskowroclaw.pl/displaywp_project/nelson-10117/"></a></li>
                  </ul>
                </div>
                <div class="filter-cover">
                  <img src="http://schroniskowroclaw.pl/wp-content/uploads/2017/02/DSCF9115.jpg" alt="project">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="container">
    <ul class="page-numbers">
    	<li><span class="page-numbers current">1</span></li>
    	<li><a class="page-numbers" href="http://schroniskowroclaw.pl/zwierzeta-do-adopcji/?page=2">2</a></li>
    	<li><a class="page-numbers" href="http://schroniskowroclaw.pl/zwierzeta-do-adopcji/?page=3">3</a></li>
    	<li><a class="page-numbers" href="http://schroniskowroclaw.pl/zwierzeta-do-adopcji/?page=4">4</a></li>
    	<li><a class="next page-numbers" href="http://schroniskowroclaw.pl/zwierzeta-do-adopcji/?page=2">→</a></li>
    </ul>
  </div>
</div>
'''

animal_html = '''
<div class="project">
  <div class="row">
    <div class="span7">
      <div class="project-cover">
        <div class="project-slider" data-tesla-plugin="slider" data-tesla-item=">img" style="position: relative; height: 475px;">
          <img src="http://schroniskowroclaw.pl/wp-content/uploads/2017/02/DSCF9115.jpg" class="attachment-full size-full" alt="DSCF9115" srcset="http://schroniskowroclaw.pl/wp-content/uploads/2017/02/DSCF9115.jpg 1853w, http://schroniskowroclaw.pl/wp-content/uploads/2017/02/DSCF9115-768x930.jpg 768w" sizes="(max-width: 1853px) 100vw, 1853px" style="position: absolute; top: 0px; left: 0px; right: 0px; z-index: 0; display: block;" width="1853" height="2246">
          <img src="http://schroniskowroclaw.pl/wp-content/uploads/2017/02/DSCF9120.jpg" class="attachment-full size-full" alt="DSCF9120" srcset="http://schroniskowroclaw.pl/wp-content/uploads/2017/02/DSCF9120.jpg 2953w, http://schroniskowroclaw.pl/wp-content/uploads/2017/02/DSCF9120-768x581.jpg 768w" sizes="(max-width: 2953px) 100vw, 2953px" style="position: absolute; top: 0px; left: 0px; right: 0px; z-index: 0; display: none;" width="2953" height="2237">
          <div class="prev">‹</div>
          <div class="next">›</div>
        </div>
      </div>
    </div>
    <div class="span5">
      <div class="project-details">
        <ul class="project-selection">
          <li><a href="http://schroniskowroclaw.pl/displaywp_project/gloria-9417/" rel="prev">Wstecz</a></li>
        </ul>
        <h1>Nelson (101/17)</h1>
        <ul class="project-info">
          <li><span>101/17</span>Nr. ew.</li>
          <li><span>18.02.2017</span>W schronisku od</li>
          <li><span>Koty</span>Kategoria</li>
        </ul>
        <p>Nelson ma 4-lata, został oddany. Duży, gruby, piękny kocur. Wykastrowany.</p>
        <p>Będzie do adopcji od: 4.03.2017</p>
        <br>
        <div class="share-it">
          <span>Udostępnij</span>
          <ul>
            <li><span class="st_facebook"></span></li>
            <li><span class="st_twitter"></span></li>
            <li><span class="st_googleplus"></span></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</div>
'''


class TestSchroniskoWroclawPl(unittest.TestCase, metaclass=AsyncMeta):

    def setUp(self):
        self.shelter = fetch.SchroniskoWroclawPl()

    @unittest.skip
    async def test_parse(self):
        self.fail()

    async def test__animals_urls(self):
        animals = ['http://schroniskowroclaw.pl/displaywp_project/burbon-22117/',
                   'http://schroniskowroclaw.pl/displaywp_project/nelson-10117/']
        urls = []

        with mock.patch.object(ClientSession, 'get', return_value=f_resp(all_animals)) as mock_get:
            async with ClientSession() as session:
                self.shelter.session = session
                # TODO Pyflakes doesn't support async comprehension
                async for url in self.shelter._animals_urls():
                    urls.append(url)

            self.assertListEqual(urls, animals)
            self.assertEqual(mock_get.call_count, 2)

            mock_get.assert_any_call(self.shelter.start_url)
            mock_get.assert_any_call('http://schroniskowroclaw.pl/zwierzeta-do-adopcji/?page=2')

    async def test__animals_urls_invalid_html(self):
        urls = []

        with mock.patch.object(ClientSession, 'get', return_value=f_resp('Invalid')) as mock_get:
            async with ClientSession() as session:
                self.shelter.session = session
                # TODO Pyflakes doesn't support async comprehension
                async for url in self.shelter._animals_urls():
                    urls.append(url)

            mock_get.assert_called_once_with(self.shelter.start_url)
            self.assertListEqual([], urls)

    def test__parse(self):
        valid_data = {
            'name': 'Nelson',
            'id': '101/17',
            'photos': ['http://schroniskowroclaw.pl/wp-content/uploads/2017/02/DSCF9115.jpg',
                       'http://schroniskowroclaw.pl/wp-content/uploads/2017/02/DSCF9120.jpg'],
            'since': '18.02.2017',
            'category': 'Koty',  # TODO i18n
            'description': ['Nelson ma 4-lata, został oddany. Duży, gruby, piękny kocur. Wykastrowany.',
                            'Będzie do adopcji od: 4.03.2017']
        }
        data = self.shelter._parse(animal_html)
        self.assertDictEqual(data, valid_data)

    def test__parse_invalid_html(self):
        data = self.shelter._parse('')
        self.assertDictEqual(data, {})
