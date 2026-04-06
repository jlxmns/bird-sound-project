import birdnet

model = birdnet.load("acoustic", "2.4", "tf")

predictions = model.predict("test_audios/portal_do_sol.wav")

predictions.to_csv("portal_do_sol.csv")
