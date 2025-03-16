'use client';

import { useState, useEffect, useRef } from 'react';
import { MessageCircle, X, Send } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { FastApiLink } from '@/lib/constants';

interface Message {
  content: string;
  isUser: boolean;
  timestamp: Date;
}

export function ChatInterface() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [hasSeenWelcome, setHasSeenWelcome] = useState(false);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check if user has seen welcome message before
  useEffect(() => {
    const welcomeSeen = localStorage.getItem('welcomeSeen') === 'true';
    setHasSeenWelcome(welcomeSeen);
  }, []);

  // Fetch welcome message when chat is first opened
  useEffect(() => {
    const initialMessage: Message = {content: "Hello! I'm Tecco, your technical assistant here to help you with building personal computers. If you're looking for component recommendations or have any questions about assembling a PC, feel free to ask me!", isUser: false, timestamp: new Date() } 
    setMessages([initialMessage ])
  }, [isOpen, hasSeenWelcome]);

  const sendMessage = async (messageText: string) => {
    if (!messageText.trim()) return;
    
    // Add user message to chat
    const userMessage: Message = {
      content: messageText,
      isUser: true,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    
    try {
      const response = await fetch(`${FastApiLink}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: messageText }),
      });
      
      const data = await response.json();
      
      // Add assistant response to chat
      const assistantMessage: Message = {
        content: data.assistant_response,
        isUser: false,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message to chat
      const errorMessage: Message = {
        content: "Sorry, I couldn't process your message. Please try again later.",
        isUser: false,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePredefinedOption = (option: string) => {
    sendMessage(option);
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      {isOpen && (
        <Card className="mb-12 w-80 md:w-96 shadow-lg">
          <CardHeader className="p-3 border-b flex justify-between items-center">
            <h3 className="font-medium justify-center">Ask Tecco</h3>
            <Button 
              variant="ghost" 
              size="icon" 
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
            >
              <X className="hover:cursor-pointer h-4 w-4" />
            </Button>
          </CardHeader>
          
          <CardContent className="p-3 h-80 overflow-y-auto">
            {messages.length === 0 && !isLoading ? (
              <div className="flex flex-col gap-2 h-full justify-center items-center text-center text-muted-foreground">
                <MessageCircle className="h-8 w-8 mb-2" />
                <p>How can I help you today?</p>
                <div className="flex flex-col gap-2 mt-4 w-full">
                  <Button 
                    variant="outline" 
                    onClick={() => handlePredefinedOption("I need a PC for gaming.")}
                    className="justify-start"
                  >
                    I need a PC for gaming
                  </Button>
                </div>
              </div>
            ) : (
              <>
                {messages.map((message, index) => (
                  <div 
                    key={index} 
                    className={`mb-3 ${message.isUser ? 'text-right' : 'text-left'}`}
                  >
                    <div 
                      className={`inline-block px-3 py-2 rounded-lg ${
                        message.isUser 
                          ? 'bg-primary text-primary-foreground' 
                          : 'bg-muted text-muted-foreground'
                      }`}
                    >
                      {message.content}
                    </div>
                    <div className="text-xs text-muted-foreground mt-1">
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="text-left mb-3">
                    <div className="inline-block px-3 py-2 rounded-lg bg-muted">
                      <div className="flex gap-1">
                        <div className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce" style={{ animationDelay: '0ms' }}></div>
                        <div className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce" style={{ animationDelay: '150ms' }}></div>
                        <div className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce" style={{ animationDelay: '300ms' }}></div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </>
            )}
          </CardContent>
          
          <CardFooter className="p-3 border-t">
            <form 
              className="flex w-full gap-2" 
              onSubmit={(e) => {
                e.preventDefault();
                sendMessage(inputValue);
              }}
            >
              <Input
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Type your message..."
                disabled={isLoading}
                className="flex-1"
              />
              <Button 
                type="submit" 
                size="icon" 
                disabled={isLoading || !inputValue.trim()}
                aria-label="Send message"
                className='bg-[#8CD50B] text-white hover:cursor-pointer'
              >
                <Send className="h-4 w-4  " />
              </Button>
            </form>
          </CardFooter>
        </Card>
      )}
      
      <Button
        onClick={() => setIsOpen(!isOpen)}
        size="icon"
        className="h-12 w-12 hover:cursor-pointer rounded-full shadow-lg fixed bottom-4 right-4 bg-[#8CD50B] hover:bg-[#7BC00A] text-white"
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        <MessageCircle className="h-6 w-6" />
      </Button>
    </div>
  );
}
