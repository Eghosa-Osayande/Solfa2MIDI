# Audiolizer: An Algorithmic Approach to Tonic Solfa Music Composition with Real-Time Playback and MIDI Export

## Demo
https://github.com/user-attachments/assets/eae2d5d3-02ce-4830-aa9b-233fcca603a2

## Abstract
Staff notation is the most popular music notation in the world (Burkholder, Grout & Palisca, 2019). However, other music notations, such as tonic solfa, emerged with a focus on facilitating the development of better relative pitch and sight-singing skills for musicians (Rainbow, 1989). Despite the advantages tonic solfa notation offers, its adoption in the music community has been relatively slow and limited. One reason for this is the initial difficulty that budding musicians face in sight-singing (Killian & Henry, 2005).

This research work addresses this issue. We developed an algorithm that parses music written in tonic solfa notation from text files into MIDI files. Additionally, we created an online web-based editor using the Flutter framework that implements the algorithm, enabling users to compose music using tonic solfa notation. The editor is equipped with playback functionality, allowing users to hear the output of their compositions in MIDI format. It also supports the export of music scores in both PDF and MIDI formats, facilitating the easy sharing of music.

## Contributions to the field:
- A web-based tonic solfa music editor created with Flutter. Available at [https://solfacity.com/app/playbook](https://solfacity.com/app/playbook)
- A Dart package for generating MIDI files, as none previously existed. Available at [https://pub.dev/packages/midi_util](https://pub.dev/packages/midi_util)

## Future work:
- Audio playback of music scores with human vocalization of tonic solfa notes

### References
Burkholder, J.P., Grout, D.J. & Palisca, C.V. (2019). *A History of Western Music* (10th ed.). W.W. Norton & Company.

Rainbow, B. (1989). *Four Centuries of Music Teaching Manuals, 1518-1932* (Vol. 1). Boethius Press.

Killian, J.N. & Henry, M.L. (2005). A comparison of successful and unsuccessful sight-singing strategies in relation to age and experience. *Journal of Research in Music Education*, 53(1), 51-65.
