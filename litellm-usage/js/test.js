const { OpenAI } = require('openai');

const TEAM_API_KEY = "************";
const PROXY_ENDPOINT = "https://nova-litellm-proxy.onrender.com";

const openai = new OpenAI({
  apiKey: TEAM_API_KEY,
  baseURL: PROXY_ENDPOINT
});

async function main() {
  const chatCompletion = await openai.chat.completions.create({
    messages: [{ role: 'user', content: 'How are you?' }],
    model: 'openai/gpt-4o',
  });
  console.log(chatCompletion.choices[0].message.content);
}

main();

