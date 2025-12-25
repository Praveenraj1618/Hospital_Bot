import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import {
  Calendar,
  MessageSquare,
  Users,
  Shield,
  Award,
  CheckCircle2,
  Star,
  ArrowRight,
  Stethoscope,
  Activity,
} from "lucide-react"
import { SiteHeader } from "@/components/site-header"
import { SiteFooter } from "@/components/site-footer"
import CurvedLoop from "@/components/curved-loop"

export default function HomePage() {
  return (
    <div className="min-h-screen">
      <SiteHeader />

      {/* Hero Section */}
      <section className="pt-32 pb-24 px-6 bg-gradient-to-br from-blue-50 via-white to-cyan-50 relative overflow-hidden">
        {/* Background decorative elements */}
        <div className="absolute top-20 right-10 w-72 h-72 bg-blue-300/20 rounded-full blur-3xl animate-pulse" />
        <div
          className="absolute bottom-20 left-10 w-96 h-96 bg-cyan-300/20 rounded-full blur-3xl animate-pulse"
          style={{ animationDelay: "1s" }}
        />

        <div className="container mx-auto max-w-7xl relative z-10">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="space-y-8">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-100 to-cyan-100 rounded-full border border-blue-200">
                <Award className="w-4 h-4 text-blue-600" />
                <span className="text-sm font-semibold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
                  Award-Winning Healthcare
                </span>
              </div>

              <h1 className="text-6xl lg:text-7xl font-bold tracking-tight text-balance leading-tight">
                Compassionate{" "}
                <span className="bg-gradient-to-r from-blue-600 via-cyan-500 to-teal-400 bg-clip-text text-transparent">
                  care
                </span>
                , exceptional{" "}
                <span className="bg-gradient-to-r from-blue-600 via-cyan-500 to-teal-400 bg-clip-text text-transparent">
                  results
                </span>
              </h1>

              <p className="text-xl text-gray-600 max-w-xl text-pretty leading-relaxed">
                Our team of experienced doctors and healthcare professionals are committed to providing quality care and
                personalized attention to our patients.
              </p>

              <div className="flex flex-wrap items-center gap-4 text-sm">
                <div className="flex items-center gap-2 px-3 py-2 bg-green-50 rounded-lg">
                  <CheckCircle2 className="w-5 h-5 text-green-600" />
                  <span className="font-medium text-green-700">24/7 Support</span>
                </div>
                <div className="flex items-center gap-2 px-3 py-2 bg-blue-50 rounded-lg">
                  <CheckCircle2 className="w-5 h-5 text-blue-600" />
                  <span className="font-medium text-blue-700">Expert Doctors</span>
                </div>
                <div className="flex items-center gap-2 px-3 py-2 bg-purple-50 rounded-lg">
                  <CheckCircle2 className="w-5 h-5 text-purple-600" />
                  <span className="font-medium text-purple-700">Modern Facilities</span>
                </div>
              </div>

              <div className="flex flex-wrap gap-4 pt-4">
                <Button
                  size="lg"
                  asChild
                  className="bg-gradient-to-r from-blue-600 via-cyan-500 to-teal-400 hover:from-blue-700 hover:via-cyan-600 hover:to-teal-500 shadow-xl shadow-blue-500/30 hover:shadow-blue-500/50 text-base h-14 px-8 transition-all hover:scale-105"
                >
                  <Link href="/book">
                    <Calendar className="w-5 h-5 mr-2" />
                    Book Appointment
                  </Link>
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  asChild
                  className="border-2 border-gray-300 hover:border-blue-500 hover:bg-blue-50 text-base h-14 px-8 bg-white hover:scale-105 transition-all"
                >
                  <Link href="/contact">
                    <MessageSquare className="w-5 h-5 mr-2" />
                    Chat with Us
                  </Link>
                </Button>
              </div>

              {/* Trust indicators */}
              <div className="flex items-center gap-8 pt-4">
                <div>
                  <div className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
                    150K+
                  </div>
                  <div className="text-xs text-gray-600">Happy Patients</div>
                </div>
                <div className="h-12 w-px bg-gray-300" />
                <div>
                  <div className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
                    50+
                  </div>
                  <div className="text-xs text-gray-600">Expert Doctors</div>
                </div>
                <div className="h-12 w-px bg-gray-300" />
                <div>
                  <div className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
                    20+
                  </div>
                  <div className="text-xs text-gray-600">Years Experience</div>
                </div>
              </div>
            </div>

            <div className="relative">
              <div className="relative rounded-3xl overflow-hidden shadow-2xl shadow-blue-500/20">
                <img
                  src="/professional-doctor-consulting-with-happy-family-i.jpg"
                  alt="Doctor consultation with happy family"
                  className="w-full h-auto"
                />
              </div>

              {/* Floating stat card - top right */}
              <Card className="absolute -top-6 -right-6 p-5 bg-white shadow-2xl border-0 hover:scale-105 transition-all">
                <div className="flex items-center gap-4">
                  <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-600 via-cyan-500 to-teal-400 flex items-center justify-center shadow-lg">
                    <Users className="w-7 h-7 text-white" />
                  </div>
                  <div>
                    <div className="text-3xl font-bold text-gray-900">150K+</div>
                    <div className="text-sm text-gray-600">Patients Recovered</div>
                  </div>
                </div>
              </Card>

              {/* Floating rating card - bottom left */}
              <Card className="absolute -bottom-6 -left-6 p-5 bg-white shadow-2xl border-0 hover:scale-105 transition-all">
                <div className="flex items-center gap-4">
                  <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-amber-400 via-orange-400 to-orange-500 flex items-center justify-center shadow-lg">
                    <Star className="w-7 h-7 text-white fill-white" />
                  </div>
                  <div>
                    <div className="text-3xl font-bold text-gray-900">4.9/5</div>
                    <div className="text-sm text-gray-600">Patient Rating</div>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      <section className="relative bg-white py-8">
        <CurvedLoop
          marqueeText="Expert Care • Modern Facilities • Your Health • Our Priority"
          speed={1.5}
          curveAmount={150}
          className="fill-[#0ea5e9]"
        />
      </section>

      {/* Features Section */}
      <section className="py-24 px-6 bg-white">
        <div className="container mx-auto max-w-7xl">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-100 to-cyan-100 rounded-full mb-4">
              <Shield className="w-4 h-4 text-blue-600" />
              <span className="text-sm font-semibold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
                Why Choose Us
              </span>
            </div>
            <h2 className="text-5xl font-bold mb-6 text-balance">
              Why Choose{" "}
              <span className="bg-gradient-to-r from-blue-600 via-cyan-500 to-teal-400 bg-clip-text text-transparent">
                ProHealth
              </span>
              ?
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto text-pretty leading-relaxed">
              We provide comprehensive healthcare services with a focus on quality, convenience, and patient
              satisfaction
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <Card className="group p-8 border-0 shadow-lg hover:shadow-2xl transition-all hover:-translate-y-2 bg-gradient-to-br from-blue-50 to-cyan-50 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-blue-200/30 rounded-full blur-2xl" />
              <div className="relative">
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-600 via-cyan-500 to-teal-400 flex items-center justify-center mb-6 shadow-lg shadow-blue-500/30 group-hover:scale-110 transition-transform">
                  <Calendar className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-2xl font-bold mb-4 text-gray-900">Easy Booking</h3>
                <p className="text-gray-600 leading-relaxed mb-4">
                  Book appointments instantly with our simple online booking system. Choose your preferred doctor and
                  time slot.
                </p>
                <Link
                  href="/book"
                  className="inline-flex items-center gap-2 text-blue-600 font-medium hover:gap-3 transition-all"
                >
                  Learn more <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            </Card>

            <Card className="group p-8 border-0 shadow-lg hover:shadow-2xl transition-all hover:-translate-y-2 bg-gradient-to-br from-teal-50 to-emerald-50 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-teal-200/30 rounded-full blur-2xl" />
              <div className="relative">
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-teal-600 via-emerald-500 to-green-400 flex items-center justify-center mb-6 shadow-lg shadow-teal-500/30 group-hover:scale-110 transition-transform">
                  <Stethoscope className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-2xl font-bold mb-4 text-gray-900">Expert Doctors</h3>
                <p className="text-gray-600 leading-relaxed mb-4">
                  Our team consists of highly qualified and experienced healthcare professionals dedicated to your
                  wellbeing.
                </p>
                <Link
                  href="/services"
                  className="inline-flex items-center gap-2 text-teal-600 font-medium hover:gap-3 transition-all"
                >
                  Learn more <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            </Card>

            <Card className="group p-8 border-0 shadow-lg hover:shadow-2xl transition-all hover:-translate-y-2 bg-gradient-to-br from-purple-50 to-pink-50 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-purple-200/30 rounded-full blur-2xl" />
              <div className="relative">
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-purple-600 via-pink-500 to-rose-400 flex items-center justify-center mb-6 shadow-lg shadow-purple-500/30 group-hover:scale-110 transition-transform">
                  <Activity className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-2xl font-bold mb-4 text-gray-900">24/7 Care</h3>
                <p className="text-gray-600 leading-relaxed mb-4">
                  Round-the-clock emergency services and support. We're always here when you need us most.
                </p>
                <Link
                  href="/contact"
                  className="inline-flex items-center gap-2 text-purple-600 font-medium hover:gap-3 transition-all"
                >
                  Learn more <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 px-6 bg-gradient-to-br from-blue-600 via-cyan-500 to-teal-400 text-white relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-white/10 rounded-full blur-3xl" />
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-white/10 rounded-full blur-3xl" />

        <div className="container mx-auto max-w-4xl text-center relative z-10">
          <h2 className="text-5xl font-bold mb-6 text-balance">Ready to Get Started?</h2>
          <p className="text-xl mb-10 opacity-90 max-w-2xl mx-auto text-pretty leading-relaxed">
            Book your appointment today and experience quality healthcare with compassionate professionals
          </p>
          <div className="flex flex-wrap gap-4 justify-center">
            <Button
              size="lg"
              variant="secondary"
              asChild
              className="h-14 px-8 text-base hover:scale-105 transition-all shadow-xl"
            >
              <Link href="/book">
                <Calendar className="w-5 h-5 mr-2" />
                Book Appointment Now
              </Link>
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="bg-white/10 hover:bg-white/20 border-2 border-white text-white h-14 px-8 text-base hover:scale-105 transition-all"
              asChild
            >
              <Link href="/services">View Our Services</Link>
            </Button>
          </div>
        </div>
      </section>

      <SiteFooter />
    </div>
  )
}
