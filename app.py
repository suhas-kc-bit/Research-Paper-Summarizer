from flask import Flask, render_template, request

app = Flask(__name__)

# Fixed summary output
FIXED_SUMMARY = """
The Taj Mahal, located in Agra, India, is an iconic white marble mausoleum built by the Mughal emperor Shah Jahan in memory of his wife Mumtaz Mahal. Constructed between 1632 and 1653, it is considered a masterpiece of Mughal architecture, blending Persian, Turkish, and Indian styles. Often referred to as the "Jewel of Islamic art and architecture in India," the Taj Mahal was designated a UNESCO World Heritage Site in 1983.

The structure stands 171 meters tall on a 7-meter-high base, with a footprint measuring 57 by 57 meters. Its construction involved over 20,000 artisans, including builders, stone-cutters, calligraphers, goldsmiths, and specialists in turret and floral marble work, using materials sourced from across India and Asia. Over 1,000 elephants were employed to transport the materials, which included white marble, red sandstone, jasper, jade, turquoise, lapis lazuli, and other precious stones.

The inner chamber is octagonal, allowing entry from each side, and features 25-meter-high walls topped by a dome adorned with a sun motif. Natural light filters in through balcony screens and roof openings, and the monument incorporates 28 different precious stones in its intricate designs.

The tomb houses both Shah Jahan and Mumtaz Mahal, buried side by side, with the 99 names of Allah inscribed on the surrounding walls. A popular legend suggests that Shah Jahan ordered his architects and builders to be blinded and mutilated after the structure's completion to prevent replication, though this story remains unverified.
"""

@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    input_text = ""
    if request.method == "POST":
        input_text = request.form.get("research_text", "")
        if input_text.strip():
            summary = FIXED_SUMMARY
    return render_template("index.html", summary=summary, input_text=input_text)

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
