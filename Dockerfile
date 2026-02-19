FROM node:24-slim AS tailwind

WORKDIR /usr/src
RUN npm install tailwindcss @tailwindcss/cli flowbite

COPY /static/css/styles.css .
RUN npx @tailwindcss/cli -i /usr/src/styles.css -o /usr/src/output.css -m

FROM python:3.11

# Install Cloudfared
# Add cloudflare gpg key
RUN mkdir -p --mode=0755 /usr/share/keyrings
RUN curl -fsSL https://pkg.cloudflare.com/cloudflare-public-v2.gpg | tee /usr/share/keyrings/cloudflare-public-v2.gpg >/dev/null

# Add this repo to your apt repositories
RUN echo 'deb [signed-by=/usr/share/keyrings/cloudflare-public-v2.gpg] https://pkg.cloudflare.com/cloudflared any main' | tee /etc/apt/sources.list.d/cloudflared.list

# install cloudflared
RUN apt-get update
RUN apt-get install cloudflared

# Set CWD & copy files
WORKDIR /usr/src/app
COPY . .
COPY --from=tailwind /usr/src/output.css /usr/src/app/static/css/

# Install requirements
RUN pip install -r requirements.txt

RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]