# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
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

import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import pydeck as pdk

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to Streamlit! 👋")

    st.sidebar.write('sidebar text')

    # Import data
    df = pd.read_csv('./MyEBirdData.csv')

    label_data = df[['Common Name', 'Latitude', 'Longitude', 'Count', 'Date', 'Location']]

    # Group data by long / lat
    df['species_and_count'] = df['Common Name'] + ': ' + df['Count'].astype(str)

    #label_data= df.groupby(['Longitude', 'Latitude']).agg(Species=('species_and_count', lambda x: '<br>'.join(x)), Count=('Count', 'sum')).reset_index()
    
    label_data = df.groupby(['Longitude', 'Latitude'])[['Date', 'species_and_count','Count']].apply(
        lambda x: pd.Series({
            'Label': '<h7>' + x['Date'] + ':</h7><p style="display:inline-block;margin:1em;margin-top: -20px;">' + '<br>'.join(x['species_and_count']) + '</p>',
            'Count': sum(x['Count'])
        })
    ).reset_index()

    label_data['Label'] = label_data['Label'].astype(str)
    
    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state = pdk.ViewState(
            longitude=-94.6708,
            latitude=38.9822,
            zoom=3
        ),
        layers = [
            pdk.Layer(
                'ScatterplotLayer',
                label_data,
                get_position=['Longitude','Latitude'],
                opacity=0.8,
                stroked=True,
                filled=True,
                radius_scale=50,
                radius_min_pixels=5,
                radius_max_pixels=20,
                line_width_min_pixels=1,
                get_radius='Count',
                pickable=True,
                get_fill_color=[255, 140, 0],
                get_line_color=[0, 0, 0]
            )
        ],
        tooltip={"html": "{Label}"}
    ))

if __name__ == "__main__":
    run()
