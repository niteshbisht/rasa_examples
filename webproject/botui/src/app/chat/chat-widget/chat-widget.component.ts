import { Component, ElementRef, HostListener, Input, OnInit, ViewChild } from '@angular/core'
import { Subject } from 'rxjs'
import { fadeIn, fadeInOut } from '../animations'
import { HttpClient } from '@angular/common/http';

const randomMessages = [
  'Nice to meet you',
  'How are you?',
  'Not too bad, thanks',
  'What do you do?',
  'Is there anything else I can help you with?',
  'That\'s awesome',
  'Angular Elements is the bomb 💣 ',
  'Can you explain in more detail?',
  'Anyway I\'ve gotta go now',
  'It was a pleasure to chat with you',
  'We are happy to make you a custom offer!',
  'Bye',
  ':)',
]

const rand = max => Math.floor(Math.random() * max)

const getRandomMessage = () => randomMessages[rand(randomMessages.length)]

@Component({
  selector: 'chat-widget',
  templateUrl: './chat-widget.component.html',
  styleUrls: ['./chat-widget.component.css'],
  animations: [fadeInOut, fadeIn],
})
export class ChatWidgetComponent implements OnInit {
  @ViewChild('bottom') bottom: ElementRef
  @Input() public theme: 'blue' | 'grey' | 'red' = 'blue'

  public _visible = false

  public get visible() {
    return this._visible
  }

  @Input() public set visible(visible) {
    this._visible = visible
    if (this._visible) {
      setTimeout(() => {
        this.scrollToBottom()
        this.focusMessage()
      }, 0)
    }
  }

  public focus = new Subject()

  public operator = {
    name: 'Operator',
    status: 'online',
    avatar: `https://randomuser.me/api/portraits/women/${rand(100)}.jpg`,
  }

  public client = {
    name: 'Guest User',
    status: 'online',
    avatar: `https://randomuser.me/api/portraits/men/${rand(100)}.jpg`,
  }

  public messages = []

  constructor(private httpClient: HttpClient) {
  }

  public addMessage(from, text, type: 'received' | 'sent') {
    this.messages.unshift({
      from,
      text,
      type,
      date: new Date().getTime(),
    })
    setTimeout(()=> this.scrollToBottom(), 90);
  }

  public scrollToBottom() {
    if (this.bottom !== undefined) {
      this.bottom.nativeElement.scrollIntoView()
    }
  }

  public focusMessage() {
    this.focus.next(true)
  }

  public randomMessage() {
    this.addMessage(this.operator, getRandomMessage(), 'received')
  }

  ngOnInit() {
    setTimeout(() => this.visible = true, 1000)
    setTimeout(() => {
      this.addMessage(this.operator, 'Hi, how can we help you?', 'received')
    }, 1500)
  }

  public toggleChat() {
    this.visible = !this.visible
  }

  public sendMessage({ message }) {
    if (message.trim() === '') {
      return
    }
    this.addMessage(this.client, message, 'sent')
    this.sendMessageToAPI(message);
    //setTimeout(() => this.randomMessage(), 1000)
  }

  sendMessageToAPI(messageText: string) {
    if (messageText && messageText.trim().toLowerCase() === 'stop') {
      messageText = '/restart';
    }
    let message = {
      "sender": "Rasa",
      "message": messageText
    };

    this.httpClient.post('/webhooks/rest/webhook', message).subscribe(
      resp => {
        console.log(resp);
        
        if (resp["0"] && resp["0"].text) {
          let keys = Object.keys(resp);
          for(let i in keys){
            this.addMessage(this.operator, resp[keys[i]].text, 'received');
          }
        }
        if (messageText === '/restart') {
          this.addMessage(this.operator, 'you can start a new conversation', 'received');
        }
      }
    );
  }

  @HostListener('document:keypress', ['$event'])
  handleKeyboardEvent(event: KeyboardEvent) {
    if (event.key === '/') {
      this.focusMessage()
    }
    if (event.key === '?' && !this._visible) {
      this.toggleChat()
    }
  }

}
