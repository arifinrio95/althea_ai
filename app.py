from flask import Flask, request, render_template, session, redirect, url_for
import openai

app = Flask(__name__)
app.secret_key = '12345'  # Ganti dengan kunci rahasia yang sesungguhnya

openai.api_key = "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"  # Masukkan API key OpenAI Anda di sini

class DokterAI:
    def __init__(self, messages):
        self.messages = messages

    def get_reply(self, question):
        prompt = """Jika saya memberikan pernyataan selain terkait medis, jangan jawab dan langsung arahkan untuk memberikan pertanyaan medis.
                    Jika saya memberikan symptomps: berikan satu follow-up pertanyaan satu-persatu secara kreatif misal dari kebiasaan, riwayat,
                    dan lainnya sampai kamu bisa mendiagnosa penyakit saya dengan pasti,
                    jangan mendiagnosa jika kesimpulannya belum pasti.
                    Setelah mendiagnosis, sertakan sumber jurnal ilmiah atau paper yang mendukung beserta kutipannya yang related.
                    Setelah mendiagnosis, berikan saran penangangan jika kondisi memungkinkan.
                    Jika belum bisa mendiagnosis, balas dengan pertanyaan follow up.
                    Respon dengan gaya non formal seperti teman dan seolah kamu manusia yang memiliki empati.
                    Saya akan merespon dengan Bahasa Indonesia, menggunakan kata ganti kamu instead of Anda.
                    Tidak usah memberi tahu saya untuk menghubungi dokter."""

        self.messages.append({"role": "user", "content": question})
        self.messages.append({"role": "system", "content": prompt})

        response = openai.ChatCompletion.create(
            model='gpt-4',
            # model="gpt-3.5-turbo",
            messages=self.messages
        )
        answer = response['choices'][0]['message']['content']
        self.messages.append({"role": "assistant", "content": answer})
        return answer

@app.route("/", methods=["GET", "POST"])
def home():
    if 'messages' not in session:
        session['messages'] = [
            {"role": "system", "content": "Saya adalah DokterAI, dokter virtualmu. Saya siap membantumu dengan pertanyaan medis kamu. Saya akan merespon dengan Bahasa Indonesia."}
        ]

    if request.method == "POST":
        user_input = request.form.get("user_input")
        bot = DokterAI(session['messages'])
        response = bot.get_reply(user_input)
        session['messages'] = bot.messages
        return redirect(url_for('home'))

    return render_template("home.html", messages=session['messages'])

@app.route("/reset", methods=["POST"])
def reset():
    session.clear()  # Menghapus seluruh session
    return redirect(url_for('home'))  # Mengarahkan kembali ke home
    
if __name__ == "__main__":
    app.run(debug=True)
