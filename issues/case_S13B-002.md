# Tab content resets when an unrelated button is pressed

The app has a button labeled "rebuild parent: N" above a tab bar with two tabs ("tab 1", "tab 2"). Each tab body has a button showing "counter: N" that increments when tapped.

Steps:
1. Launch the app.
2. Tap the "counter" button twice so it shows "counter: 2".
3. Tap the "rebuild parent" button.

Expected: The tab body still shows "counter: 2".

Actual: The counter goes back to "counter: 0".
