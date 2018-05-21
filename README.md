# Chess tactical vision
Augmented chess board visualization by overlaying all possible attacks/defenses

## Introduction
Designed to aid in assessing board position and calculating tactics.

In the example output below, unmarked squares are not attacked by white. Marked squares are colored by number of white's pieces attacking it.
1 - Blue
2 - Green
3 - Yellow
4 - Orange

![EnhancedBoard](https://github.com/Mitchellpkt/Chess-Tactical-Vision/blob/master/Output_Figures/demo1-enhanced.png)

*Note the missing marks on e7 & g7. This is a known bug, filed as issue #1, feel free to fix*

## Uses

Use 1: training oneself by solving puzzles with enhanced vision

Use 2: if both parties agree in advance, playing on a field with enhanced vision for both players 

## Misc

Current implementation requires ChessNut and FEN python libraries. This is just a hacky proof of concept; presumably any applications will be re-worked based on that implementation's platform.

It would be neat to add this to Lichess studies and post-game analysis (i.e. the same pages where stockfish is enabled)

!!!! Don't be a scumbag and use this for cheating. 
