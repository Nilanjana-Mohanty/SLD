async function capture(label) {
    document.getElementById("avgDisplay").innerText = "Capturing " + label + "...";
    document.getElementById("samplesDisplay").innerText = "";

    try {
        const res = await fetch("/capture", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ label: label })
        });

        const data = await res.json();
        if (data.error) throw new Error(data.error);

        document.getElementById("samplesDisplay").innerText = JSON.stringify(data.samples, null, 2);
        document.getElementById("avgDisplay").innerText = JSON.stringify(data.average, null, 2);
    } catch (err) {
        document.getElementById("avgDisplay").innerText = "Error: " + err.message;
    }
}
