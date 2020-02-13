# Kalliope neuron launch_radio

Kalliope Project is available here: https://github.com/kalliope-project

Kalliope's documentation: https://kalliope-project.github.io/

## Synopsis

A Kalliope Neuron to launch and stop radio stations.

Made from Kalliope neuron ambient_sound, available here: https://github.com/kalliope-project/kalliope_neuron_ambient_sound

## Installation

Install the neuron into your resource directory
```bash
kalliope install --git-url https://github.com/SomebodyLikeEveryBody/kalliope_neuron_launch_radio.git
```

## Options

| parameter         | required | type   | default          | choices             | comment                                                                     |
|-------------------|----------|--------|------------------|---------------------|-----------------------------------------------------------------------------|
| state             | YES      | string |                  | "on", "off"         | Target state of the radio player.                                          |
| radio_url        | NO/YES       | string |                  | working radio_url available on internet | Need to be set if the State is "on".  |
| random_options        | NO       | string | "random-select-one" | "random-select-one", "random-order-play", "no-random" | Let the choice to play the song list: by playing one picked randomly OR play all in a random order OR play all in the listed order.  |
| mplayer_path      | NO       | string | "/usr/bin/mplayer" |                     | Path to mplayer binary. By default /usr/bin/mplayer on Debian family system |
| auto_stop_minutes | NO       | int    |                  | Integer > 1         | Number of minutes before Kalliope stop automatically the background sound   |
| loop_option | NO       | int    | "no-loop" | "no-loop", "loop"         | If we want the player to play the song in infinite loop. /!\ But beware, if you list multiple sounds in the synapse and specify loop: "no-loop", it will not loop the list but play the list and loop the last sound of the list.. The playlist management feature is clearly not finished yet. |


## Return Values

| Name             | Description                             | Type   | sample                                                   |
|------------------|-----------------------------------------|--------|----------------------------------------------------------|
| sound_name   | The given name to the played sound               | string | 'LOFI relaxing sound'        |
| sound_link | The link to the played sound | string | 'http://stream.radioneo.org:8000/;stream/1' or './resources/sounds/music/lofi.wav' |

## Synapses example

Here is a launchRadioSynapses.yml example:

```
- name: "stop-radio-synapse"
  signals:
    - order: "coupe la radio"
    - order: "stoppe la radio"
  neurons:
    - launch_radio:
        state: "off"

- name: "Launch-radio-choice-synapse"
  signals:
    - order:
        text: "passe en mode radio"
        matching-type: "ordered-strict"
  neurons:
    - say:
        message: "Quelle radio voulez-vous lancer ?"
    - neurotransmitter:
        from_answer_link:
        - synapse: "launch-radio-Neo-synapse"
          answers:
            - "Radio Néo"
        - synapse: "launch-radio-RTL-synapse"
          answers:
            - "RTL"
        - synapse: "launch-radio-classique-synapse"
          answers:
            - "Radio Classique"
        - synapse: "launch-radio-FIP-synapse"
          answers:
            - "FIP"
        - synapse: "launch-radio-Nova-synapse"
          answers:
            - "Radio Nova"
        - synapse: "launch-radio-TSF-Jazz-synapse"
          answers:
            - "TSF Jazz"
        - synapse: "launch-radio-France-Inter-synapse"
          answers:
            - "France Inter"
        - synapse: "launch-radio-France-Culture-synapse"
          answers:
            - "France Culture"
        - synapse: "launch-radio-France-Musique-synapse"
          answers:
            - "France Musique"
        default: "launch-radio-Neo-synapse"


- name: "launch-radio-Neo-synapse"
  signals:
    - order: "mets-nous Radio Néo"
    - order: "lance Radio Néo"
    - order: "lance-moi Radio Néo"
    - order: "mets-moi Radio Néo"
    - order: "mets Radio Néo"
    - order: "tu peux mettre Radio Néo"
    - order: "tu peux lancer Radio Néo"
  neurons:
    - launch_radio:
        state: "on"
        radio_url: "http://stream.radioneo.org:8000/;stream/1"
        radio_name: "Radio Néo"
    - say:
        message: "Radio Néo lancée."


- name: "launch-radio-RTL-synapse"
  signals:
    - order: "mets-nous RTL"
    - order: "lance RTL"
    - order: "lance-moi RTL"
    - order: "mets-moi RTL"
    - order: "mets RTL"
    - order: "tu peux mettre RTL"
    - order: "tu peux lancer RTL"
  neurons:
    - launch_radio:
        state: "on"
        radio_url: "http://streaming.radio.rtl.fr/rtl-1-48-192"
        radio_name: "RTL"
    - say:
        message: "Radio RTL lancée."

- name: "launch-radio-classique-synapse"
  signals:
    - order: "mets-nous Radio Classique"
    - order: "lance Radio Classique"
    - order: "lance-moi Classique"
    - order: "mets-moi Classique"
    - order: "mets Radio Classique"
    - order: "tu peux mettre Radio Classique"
    - order: "tu peux lancer Radio Classique"
  neurons:
    - launch_radio:
        state: "on"
        radio_url: "http://radioclassique.ice.infomaniak.ch/radioclassique-high.mp3"
        radio_name: "Radio Classique"
    - say:
        message: "Radio classique lancée."

- name: "launch-radio-FIP-synapse"
  signals:
    - order: "mets-nous Radio FIP"
    - order: "lance Radio FIP"
    - order: "lance-moi Radio FIP"
    - order: "mets-moi Radio FIP"
    - order: "mets Radio FIP"
    - order: "tu peux mettre Radio FIP"
    - order: "tu peux lancer Radio FIP"
  neurons:
    - launch_radio:
        state: "on"
        radio_url: "http://direct.fipradio.fr/live/fip-midfi.mp3"
        radio_name: "Radio FIP"
    - say:
        message: "Radio FIP lancée."

- name: "launch-radio-Nova-synapse"
  signals:
    - order: "mets-nous Radio Nova"
    - order: "lance Radio Nova"
    - order: "lance-moi Radio Nova"
    - order: "mets-moi Radio Nova"
    - order: "mets Radio Nova"
    - order: "tu peux mettre Radio Nova"
    - order: "tu peux lancer Radio Nova"
  neurons:
    - launch_radio:
        state: "on"
        radio_url: "http://novazz.ice.infomaniak.ch/novazz-128.mp3"
        radio_name: "Radio Nova"
    - say:
        message: "Radio Nova lancée."

- name: "launch-radio-TSF-Jazz-synapse"
  signals:
    - order: "mets-nous TSF Jazz"
    - order: "lance TSF Jazz"
    - order: "lance-moi TSF Jazz"
    - order: "mets-moi TSF Jazz"
    - order: "mets TSF Jazz"
    - order: "tu peux mettre TSF Jazz"
    - order: "tu peux lancer TSF Jazz"
  neurons:
    - launch_radio:
        state: "on"
        radio_url: "http://direct.fipradio.fr/live/fip-midfi.mp3"
        radio_name: "TSF Jazz"
    - say:
        message: "Radio TSF Jazz lancée."

- name: "launch-radio-France-Inter-synapse"
  signals:
    - order: "mets-nous France Inter"
    - order: "lance France Inter"
    - order: "lance-moi France Inter"
    - order: "mets-moi France Inter"
    - order: "mets France Inter"
    - order: "tu peux mettre France Inter"
    - order: "tu peux lancer France Inter"
  neurons:
    - launch_radio:
        state: "on"
        radio_url: "http://direct.franceinter.fr/live/franceinter-midfi.mp3"
        radio_name: "France Inter"
    - say:
        message: "Radio France Inter lancée."

- name: "launch-radio-France-Culture-synapse"
  signals:
    - order: "mets-nous France Culture"
    - order: "lance France Culture"
    - order: "lance-moi France Culture"
    - order: "mets-moi France Culture"
    - order: "mets France Culture"
    - order: "tu peux mettre France Culture"
    - order: "tu peux lancer France Culture"
  neurons:
    - launch_radio:
        state: "on"
        radio_url: "http://direct.franceculture.fr/live/franceculture-midfi.mp3"
        radio_name: "France Culture"
    - say:
        message: "Radio France Culture lancée."

- name: "launch-radio-France-Musique-synapse"
  signals:
    - order: "mets-nous France Musique"
    - order: "lance France Musique"
    - order: "lance-moi France Musique"
    - order: "mets-moi France Musique"
    - order: "mets France Musique"
    - order: "tu peux mettre France Musique"
    - order: "tu peux lancer France Musique"
  neurons:
    - launch_radio:
        state: "on"
        radio_url: "http://direct.francemusique.fr/live/francemusique-midfi.mp3"
        radio_name: "France Musique"
    - say:
        message: "Radio France Musique lancée."
```

