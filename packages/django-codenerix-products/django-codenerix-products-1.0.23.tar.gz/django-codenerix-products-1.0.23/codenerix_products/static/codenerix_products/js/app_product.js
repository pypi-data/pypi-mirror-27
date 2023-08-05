/*
 *
 * django-codenerix-products
 *
 * Copyright 2017 Centrologic Computational Logistic Center S.L.
 *
 * Project URL : http://www.codenerix.com
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

var module = codenerix_builder(
    ['codenerixPRODUCTSControllers'],
    {
        'list0': {'': {templateUrl: get_static('codenerix_products/partials/products_list.html')}},
        'formcustom0': {'': 
            {
                url: '/custom/add',
                templateUrl: function(params) { return '/'+ws_entry_point+'/custom/add'; },
                controller: 'FormAddCtrlProductCustom'
            }
        }
    }
);
/*
    Examples:
    'list0': [undefined, get_static('codenerix_products/partials/products_list.html'), undefined]
    'list0': {'': {templateUrl: get_static('codenerix_products/partials/products_list.html')}}
*/