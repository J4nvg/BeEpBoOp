"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Plus, Minus, X, FlameIcon, ArrowLeft, ArrowRight, Check } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import Link from "next/link"
import { type Component, componentTypes } from "@/lib/types"
import { toast } from "sonner"
import { fetchCompatible, type PCConfiguration } from "@/lib/api"
import { Progress } from "@/components/ui/progress"

const sampleComponents: Component[] = [
  {
    id: 1,
    type: "cpu",
    name: "Intel Core i7-11700K",
    specs: "8 cores, 16 threads, 3.6 GHz",
    price: 320,
    recommended: true,
    link: "#",
  },
  { id: 2, type: "cpu", name: "AMD Ryzen 5 5600X", specs: "6 cores, 12 threads, 3.7 GHz", price: 280, link: "#" },
  { id: 10, type: "cpu", name: "AMD Ryzen 7 5800X", specs: "8 cores, 16 threads, 3.8 GHz", price: 350, link: "#" },
  { id: 11, type: "cpu", name: "Intel Core i5-12600K", specs: "10 cores, 16 threads, 3.7 GHz", price: 290, link: "#" },
  { id: 12, type: "cpu", name: "AMD Ryzen 9 5900X", specs: "12 cores, 24 threads, 3.7 GHz", price: 450, link: "#" },
  { id: 13, type: "cpu", name: "Intel Core i9-12900K", specs: "16 cores, 24 threads, 3.2 GHz", price: 580, link: "#" },
  { id: 14, type: "cpu", name: "AMD Ryzen 5 5600G", specs: "6 cores, 12 threads, 3.9 GHz", price: 260, link: "#" },
  { id: 15, type: "cpu", name: "Intel Core i7-12700K", specs: "12 cores, 20 threads, 3.6 GHz", price: 410, link: "#" },
  { id: 16, type: "cpu", name: "AMD Ryzen 7 5700G", specs: "8 cores, 16 threads, 3.8 GHz", price: 330, link: "#" },
  { id: 3, type: "mb", name: "ASUS Prime B550-PLUS", specs: "ATX, AM4 socket", price: 150, link: "#" },
  { id: 17, type: "mb", name: "MSI MAG B660 TOMAHAWK", specs: "ATX, LGA1700 socket", price: 180, link: "#" },
  { id: 4, type: "gpu", name: "NVIDIA RTX 3080", specs: "10GB GDDR6X", price: 699, link: "#" },
  { id: 5, type: "ram", name: "Corsair Vengeance LPX 16GB", specs: "DDR4 3200MHz", price: 80, link: "#" },
  { id: 6, type: "storage", name: "Samsung 970 EVO Plus", specs: "1TB NVMe SSD", price: 130, link: "#" },
  { id: 7, type: "psu", name: "EVGA 600W Bronze", specs: "80+ Bronze Certification", price: 60, link: "#" },
  { id: 8, type: "cooling", name: "Cooler Master Hyper 212", specs: "Air CPU Cooler", price: 35, link: "#" },
  { id: 9, type: "case", name: "NZXT H510", specs: "Mid Tower, Tempered Glass", price: 70, link: "#" },
  { id: 123, type: "case", name: "NZXT H510", price: 70, link: "#" },
]

export default function PCBuilder() {
  // Define the order of component selection
  const componentOrder = ["cpu", "mb", "gpu", "ram", "storage", "cooling", "case", "psu"]
  const [currentStep, setCurrentStep] = useState<number>(0)
  const [selectedComponents, setSelectedComponents] = useState<Record<string, Component | null>>({
    cpu: null,
    mb: null,
    gpu: null,
    ram: null,
    storage: null,
    cooling: null,
    case: null,
    psu: null,
  })
  const [searchQuery, setSearchQuery] = useState<string>("")
  const [compatibleComponents, setCompatibleComponents] = useState<Component[]>([])

  const currentComponentType = componentOrder[currentStep]
  const currentComponentLabel = componentTypes.find((type) => type.id === currentComponentType)?.label || ""
  const progress = ((currentStep + 1) / componentOrder.length) * 100

  useEffect(() => {
    const configuration: Partial<PCConfiguration> = {}
    Object.keys(selectedComponents).forEach((key) => {
      if (selectedComponents[key]) {
        configuration[key] = selectedComponents[key]!.id
      }
    })

    if (currentComponentType) {
      fetchCompatible(configuration as PCConfiguration, currentComponentType)
        .then((data) => {
          setCompatibleComponents(data)
        })
        .catch((error) => {
          console.error("Error fetching compatible components:", error)
        })
    }
  }, [currentComponentType, selectedComponents])

  // Filter components based on current step and search query
  const availableComponents = sampleComponents.filter((component) => {
    return (
      component.type === currentComponentType &&
      (component.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        component.specs?.toLowerCase().includes(searchQuery.toLowerCase()))
    )
  })

  const addToBuild = (component: Component) => {
    setSelectedComponents({
      ...selectedComponents,
      [component.type]: component,
    })

    // If not the last step, automatically move to next step
    if (currentStep < componentOrder.length - 1) {
      setCurrentStep(currentStep + 1)
      setSearchQuery("")
    }
  }

  const removeFromBuild = (componentType: string) => {
    // Reset all components that come after this one in the order
    const currentIndex = componentOrder.indexOf(componentType)
    const updatedComponents = { ...selectedComponents }

    // Reset the current component and all that follow
    for (let i = currentIndex; i < componentOrder.length; i++) {
      updatedComponents[componentOrder[i]] = null
    }

    setSelectedComponents(updatedComponents)

    // Go back to the step of the removed component
    setCurrentStep(currentIndex)
    setSearchQuery("")

    toast("Components reset", {
      description: "Later components have been reset to ensure compatibility.",
    })
  }

  const isComponentSelected = (component: Component) => {
    return selectedComponents[component.type]?.id === component.id
  }

  const totalPrice = Object.values(selectedComponents)
    .filter(Boolean)
    .reduce((sum, component) => sum + (component?.price || 0), 0)

  const allComponentsSelected = Object.values(selectedComponents).every(Boolean)

  const handleCheckout = () => {
    if (!allComponentsSelected) return

    console.log("Checkout with the following components:")
    Object.entries(selectedComponents).forEach(([type, component]) => {
      if (component) {
        console.log(`${type}: ${component.name} (ID: ${component.id})`)
      }
    })
  }

  const goToPreviousStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
      setSearchQuery("")
    }
  }

  const goToNextStep = () => {
    if (currentStep < componentOrder.length - 1 && selectedComponents[currentComponentType]) {
      setCurrentStep(currentStep + 1)
      setSearchQuery("")
    }
  }

  const goToStep = (index: number) => {
    // Can only go to steps where previous components are selected
    for (let i = 0; i < index; i++) {
      if (!selectedComponents[componentOrder[i]]) {
        return
      }
    }
    setCurrentStep(index)
    setSearchQuery("")
  }

  return (
    <div className="container mx-auto p-6 max-w-5xl">
      <h1 className="text-xl font-bold text-center">Configure your own PC</h1>

      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex justify-between mb-2">
          <span className="text-sm font-medium">
            Step {currentStep + 1} of {componentOrder.length}
          </span>
          <span className="text-sm font-medium">{currentComponentLabel}</span>
        </div>
        <Progress value={progress} className="h-2 " />
      </div>

      {/* Step Indicators */}
      <div className="grid grid-cols-4 md:grid-cols-8 gap-2 mb-8">
        {componentOrder.map((type, index) => {
          const componentType = componentTypes.find((t) => t.id === type)
          const Icon = componentType?.icon
          const isSelected = !!selectedComponents[type]
          const isCurrent = index === currentStep

          return (
            <div
              key={type}
              className={`flex flex-col items-center p-2 rounded-md cursor-pointer transition-colors
                ${isSelected ? "text-[#8CD50B]" : "text-muted-foreground"}
                ${isCurrent ? "bg-muted" : ""}
                ${index > currentStep && !selectedComponents[componentOrder[index - 1]] ? "opacity-50 cursor-not-allowed" : "hover:bg-muted/50"}
              `}
              onClick={() => goToStep(index)}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center mb-1
                ${isSelected ? "bg-[#8CD50B] text-white" : "bg-muted"}
              `}
              >
                {isSelected ? <Check className="w-4 h-4" /> : Icon && <Icon className="w-4 h-4" />}
              </div>
              <span className="text-xs truncate">{componentType?.label}</span>
            </div>
          )
        })}
      </div>

      {/* Selected Components Summary */}
      <Card className="mb-6">
        <CardHeader className="pb-2">
          <h2 className="text-lg font-semibold">Your Build</h2>
        </CardHeader>
        <CardContent className="pb-2">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {componentOrder.map((type) => {
              const componentType = componentTypes.find((t) => t.id === type)
              const Icon = componentType?.icon
              const selectedComponent = selectedComponents[type]

              return (
                <div key={type} className="flex items-center gap-2 p-2 rounded-md">
                  {Icon && <Icon className="w-5 h-5 flex-shrink-0" />}
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium">{componentType?.label}</p>
                    {selectedComponent ? (
                      <p className="text-sm truncate">{selectedComponent.name}</p>
                    ) : (
                      <p className="text-xs text-muted-foreground italic">Not selected</p>
                    )}
                  </div>
                  {selectedComponent && (
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold text-[#8CD50B]">
                        ${selectedComponent.price.toFixed(2)}
                      </span>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6 rounded-full hover:bg-destructive/50 hover:text-white"
                        onClick={() => removeFromBuild(type)}
                      >
                        <X className="h-3 w-3" />
                        <span className="sr-only">Remove {componentType?.label}</span>
                      </Button>
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </CardContent>
        <CardFooter className="flex justify-between pt-2">
          <div className="font-medium">Total:</div>
          <div className="font-bold text-[#8CD50B]">${totalPrice.toFixed(2)}</div>
        </CardFooter>
      </Card>

      {/* Current Step Component Selection */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Select {currentComponentLabel}</h2>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={goToPreviousStep} disabled={currentStep === 0}>
              <ArrowLeft className="w-4 h-4 mr-1" /> Previous
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={goToNextStep}
              disabled={currentStep === componentOrder.length - 1 || !selectedComponents[currentComponentType]}
            >
              Next <ArrowRight className="w-4 h-4 ml-1" />
            </Button>
          </div>
        </div>

        {/* Search Bar */}
        <Input
          type="text"
          placeholder={`Search ${currentComponentLabel} components...`}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full mb-4"
        />

        {/* Component List */}
        <div className="grid gap-4">
          {availableComponents.length === 0 ? (
            <div className="text-center p-4 bg-muted rounded-md">
              <p>No compatible {currentComponentLabel.toLowerCase()} components available</p>
            </div>
          ) : (
            availableComponents.map((component) => {
              const isSelected = isComponentSelected(component)

              return (
                <Card
                  key={component.id}
                  className={`hover:border-[#8CD50B] transition-colors ${isSelected ? "border-[#8CD50B]" : ""}`}
                >
                  <CardHeader className="pb-2">
                    <div className="flex justify-end text-[#8CD50B]">
                      {component.recommended ? (
                        <span className="flex items-baseline">
                          Recommended <FlameIcon className="ml-1 w-4 h-4" />
                        </span>
                      ) : null}
                    </div>
                  </CardHeader>
                  <CardContent className="flex items-center p-4">
                    <div className="w-20 h-20 bg-gray-200 rounded flex items-center justify-center mr-4">
                      {/* Placeholder for component image */}
                    </div>
                    <div className="flex-1">
                      <Link href={component.link}>
                        <h3 className="font-semibold">{component.name}</h3>
                      </Link>
                      <p className="text-sm text-gray-600">{component.specs}</p>
                    </div>
                    <div className="text-lg font-bold text-[#8CD50B]">${component.price.toFixed(2)}</div>
                  </CardContent>
                  <CardFooter className="justify-end pt-2">
                    {isSelected ? (
                      <Button variant="destructive" onClick={() => removeFromBuild(component.type)}>
                        Remove <Minus className="ml-2 h-4 w-4" />
                      </Button>
                    ) : (
                      <Button variant="outline" onClick={() => addToBuild(component)}>
                        Add to build <Plus className="ml-2 h-4 w-4" />
                      </Button>
                    )}
                  </CardFooter>
                </Card>
              )
            })
          )}
        </div>
      </div>

      {/* Checkout Button */}
      <div className="mt-8">
        <Button
          onClick={handleCheckout}
          disabled={!allComponentsSelected}
          className="w-full bg-[#8CD50B] hover:bg-[#7BC00A] text-white font-bold py-3"
        >
          Checkout
        </Button>
        {!allComponentsSelected && (
          <p className="text-sm text-muted-foreground mt-2 text-center">Complete all steps to proceed to checkout</p>
        )}
      </div>
    </div>
  )
}

